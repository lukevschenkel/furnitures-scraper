import logging
import csv
import requests
from lxml import etree
import json


class BaseScraper:
    use_debug = True
    max_retry_cnt = 5

    def __init__(self):
        try:
            self.config_log()
            self.writer = self.get_writer()
            self.session = requests.Session()
        except Exception as e:
            self.print_out(f"init: {e}")

    def get_cookies(self):
        cookies = []
        for cookie in self.driver.get_cookies():
            try:
                cookies.append(f"{cookie['name']}={cookie['value']}")
            except:
                pass
        return "; ".join(cookies)

    def validate(self, item):
        try:
            if item == None:
                item = ''
            if type(item) == list:
                item = ' '.join(item)
            item = str(item).strip()
            return item
        except:
            return ""

    def eliminate_space(self, items):
        values = []
        for item in items:
            item = self.validate(item)
            if item.lower() not in ['', ',']:
                values.append(item)
        return values

    def config_log(self):
        logging.basicConfig(
            filename=f"history.log",
            format='%(asctime)s %(levelname)-s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')
        
    def get_writer(self):
        output_file = open(
            f'{self.name}.csv',
            mode='w',
            newline='',
            encoding="utf-8-sig"
        )
        output_writer = csv.writer(
            output_file,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_ALL
        )
        output_writer.writerow(self.csv_headers)
        return output_writer
    
    def write(self, values):
        row = []
        for header in self.csv_headers:
            row.append(values.get(header, ''))
        self.writer.writerow(row)

    def print_out(self, value):
        if self.use_debug:
            print(value)
        else:
            logging.info(value)


class WayfairScraper(BaseScraper):
    scraper_api = "http://api.scraperapi.com?api_key=&url="
    base_urls = [
        ["Teen Bedroom Furniture", "https://www.wayfair.com/baby-kids/cat/teen-bedroom-furniture-c1872134.html"],
        ["Toddler & Kids Bedroom Furniture", "https://www.wayfair.com/baby-kids/cat/toddler-kids-bedroom-furniture-c215056.html"]
    ]
    site_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cookie': 'FVSID=49-6aaefee0-e4eb-4177-ab0e-b08164ac2204; ExCSNUtId=23e0884a-6656-2bc8-5d9a-3b4cc6daf002; CSNUtId=23f7265c-66c3-9943-77ef-89c6c3d77a02; canary=0; _pxvid=1a6cd621-5e5f-11ef-872f-03851baf071e; __ssid=5a977b96ef5dfb91ee447356c701e17; _gcl_gs=2.1.k1$i1724094785; sm_uuid=1724094937199; cjConsent=MHxOfDB8Tnww; cjUser=738bad57-3256-47bb-9a8e-49de1a1550af; cjLiveRampLastCall=2024-08-19T19:13:35.114Z; __podscribe_wayfair_referrer=https://www.google.com/; __podscribe_wayfair_landing_url=https://www.wayfair.com/gateway.php?refid=GX281264597885.Wayfair%7Eb&position=&network=g&pcrid=281264597885&device=c&targetid=kwd-3598608535&channel=GoogleBrand&gad_source=1&gclid=Cj0KCQjw2ou2BhCCARIsANAwM2GoZZrJuHDUOPKttruQ63KEzntBbAeOM70oDT7Xmg74smnVuCeWMJAaApUpEALw_wcB; __podscribe_did=pscrb_cbbff731-3a8d-42b6-d52d-afe2581ed528; rskxRunCookie=0; rCookie=m6nf1vvypxgp0mb9q7abwm01djelz; _gcl_au=1.1.64245698.1724094818; __attentive_id=6a15158fc9784f58a281043842ecd9b5; _attn_=eyJ1Ijoie1wiY29cIjoxNzI0MDk0ODE4ODYwLFwidW9cIjoxNzI0MDk0ODE4ODYwLFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcIjZhMTUxNThmYzk3ODRmNThhMjgxMDQzODQyZWNkOWI1XCJ9In0=; __attentive_cco=1724094818861; _tt_enable_cookie=1; _ttp=okYxR4U2Z8Qkaq4P8YcHOyATA7_; _gid=GA1.2.341556783.1724094821; _gac_UA-2081664-4=1.1724094821.Cj0KCQjw2ou2BhCCARIsANAwM2GoZZrJuHDUOPKttruQ63KEzntBbAeOM70oDT7Xmg74smnVuCeWMJAaApUpEALw_wcB; _gcl_aw=GCL.1724094821.Cj0KCQjw2ou2BhCCARIsANAwM2GoZZrJuHDUOPKttruQ63KEzntBbAeOM70oDT7Xmg74smnVuCeWMJAaApUpEALw_wcB; i18nPrefs=lang%3Den-US; salsify_session_id=1a9035a5-e169-4487-9636-4b77d082c488; CSN_CSRF=cfb0b75ec2e7b650e04cd68508f12aa88e3c7b4aa972773db3c95e8b7262999e; __attentive_dv=1; hideGoogleYolo=true; pdp-views-count=4; WFDC=IAD; vid=23f584c2-66c7-5126-6d68-2373408b3402; waychatShouldShowChatWindow=false; _dpm_ses.15e8=*; CSN=g_countryCode%3DUS%26g_zip%3D90045%26CLVW%3D6%257C132%257C128; SFSID=61bc0ba1d8b0d63b10919f97426ff2ed; serverUAInfo=%7B%22browser%22%3A%22Google%20Chrome%22%2C%22browserVersion%22%3A127%2C%22OS%22%3A%22Windows%22%2C%22OSVersion%22%3A%22%22%2C%22isMobile%22%3Afalse%2C%22isTablet%22%3Afalse%2C%22isTouch%22%3Afalse%7D; postalCode=90045; pxcts=ee030bc8-60a2-11ef-be27-b1376230fc80; _wf_fs_sample_user=true; IR_gbd=wayfair.com; __attentive_ss_referrer=https://www.wayfair.com/furniture/sb0/tv-stands-entertainment-centers-c1868409.html?itemsperpage=96&sortby=7; AppInterstitial=visit_date_1%3D2024-08-22; _pxhd=Qap7630OM8AAD8f37bUz9M7LHxrnq2vWvM8VZPpl6bqHRU9WUl7Y-ltSdOrkHId1HR8hr38cFpISKNV7vmciyA==:T6OXtaGEE07aFt5nT55SkaW69AnY32FbXTWAbwhAcIOvmH3i5RkcEweUO61DeiE3UhmPiSWDXX25iQ6i3UGX5zeH/hePfLlCwFIvWXESoss=; __cf_bm=6kaUHbYHLJx4ZKubrveYIlRKldvkSCaRhZS39btztc8-1724346220-1.0.1.1-cUU8SO4RubP2oeRbM3qug.s6NXKKET3vtYHcqXXtYIva1tsKLJlnrp.9DbbXFcanJoymzQjWrTcJGEDH2cu4Gw; _px3=6ba2c72e9fb398080990e252758ce1b10772fe83724a72d250896ba65263fa78:ynHTMrKhy2mzf0KbsMBT4WNqZxzA8xuu4XfoW7jX3lHaePDItWOcQfT6hSsoJSVo8ZUpKREwVN3Q55XLvZPlfA==:1000:gJL6QlAQyb6KuRwPg+082JgtkjN/spugKVqLfL8cfFJZrIDPm5TjoVlda/msPA+37AKNyUQaWBssyEHIOIhnQoEt8DDMw6jZSa0pOLOMTP0lvcOfvX0HTDiZ7YR2YU0f2OOFe7un9it2Nc+0XAFWtQhbhCnNkIs+Iywlm9h/H+XwMizr0jHvoofwWu0rhl5GGV9XCHXKeBlmImQoq4yXARmE9w5v6JFO2h+vTjlv4zY=; fs_lua=1.1724346222362; fs_uid=#10VS4S#ffb88c43-428d-4304-8a86-6a550a87d41a:19ab2e69-a8c4-4d75-a37a-e38a5e5c1505:1724343838945::20#/1755631072; _dpm_id.15e8=e645bdf5-2fba-46ef-8b59-5771ba08e9cc.1724094814.12.1724346223.1724313106.95f0491d-b4c5-41a3-b741-2b3702f43294; IR_12051=1724346223092%7C0%7C1724346223092%7C%7C; _ga_0GV7WXFNMT=GS1.1.1724338487.15.1.1724346223.56.0.0; _rdt_uuid=1724094815815.a52dbecd-b698-4c59-84e9-433c38b7163f; _ga_Q0HJWP456J=GS1.1.1724338491.15.1.1724346223.56.0.0; _ga=GA1.2.2106455342.1724094818; _gat_gtag_UA_2081664_4=1; lastRskxRun=1724346223633; forterToken=18810cff1bca4cd998521cc75ced14e5_1724346222601__UDF43-m4_20ck_/AEgpwq3qH4%3D-1115-v2; forterToken=18810cff1bca4cd998521cc75ced14e5_1724346222601__UDF43-m4_20ck_/AEgpwq3qH4%3D-1115-v2; __attentive_pv=33; CSNPersist=latestRefid%3DGX281264597885.Wayfair~b%26page_of_visit%3D482; otx=I/WEwmbHb2uDDyOKRJGdAg==',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }
    csv_headers = [
        'Description',
        'URL',
        'Price',
        'Reviews',
        'Rating',
        'Category',
    ]
    counts = {}
    limit = 10000
    history = []
    name = "wayfair"

    def run(self):
        try:
            self.print_out("\nStarting...")
            for base_url in self.base_urls:
                self.parse_category(base_url[1], base_url[0])
        except Exception as e:
            self.print_out(f"run: {e}")

    def parse_category(self, url, base_category=None, level=0, retry_cnt=0):
        try:
            response = self.session.get(f"{self.scraper_api}{url}", headers=self.site_headers)
            script_data = response.text.replace("\\", "")
            category_data = script_data.split('self.__next_f.push([1,"{"StoreFrontFeatureToggle')[1].split('"])')[0]
            categories = category_data.split("ProductCategory:")[1:]
            products = script_data.split("RecommendedListingCollectionItem")

            if len(products) > 10 and base_category:
                if self.counts[base_category] < self.limit and level != 0:
                    self.parse_products(url, base_category)
            else:
                if level > 2:
                    return

                for category in categories:
                    try:
                        category_name = category.split('"displayName":"')[1].split('"')[0].replace("u0026", "&")
                        category_url = category.split('"url":"')[1].split('"')[0]
                        
                        self.counts[base_category] = 0

                        self.print_out(f"Category: {category_name}, Url: {category_url}")
                        # self.parse_category(category_url, parent_category, level+1)
                        self.parse_products(category_url, base_category)
                    except:
                        pass
        except Exception as e:
            print(e)
            if retry_cnt < self.max_retry_cnt:
                self.print_out(f"Retry...{retry_cnt}")
                retry_cnt += 1
                self.parse_category(url, base_category, level, retry_cnt)

    def parse_products(self, url, base_category):
        response = self.session.get(f"{self.scraper_api}{url}?itemsperpage=96&sortby=7&curpage=0", headers=self.site_headers)
        tree = etree.HTML(response.text)
        self.parse_response(url, base_category, response)

        last_page = int(self.validate(tree.xpath(".//*[contains(@data-enzyme-id, 'paginationLastPageLink')]/text()"))) + 1
        self.print_out(f"last page: {last_page}")

        if last_page < 1:
            return

        for page_index in range(2, last_page):
            if self.counts[base_category] > self.limit:
                return

            response = self.session.get(f"{self.scraper_api}{url}?itemsperpage=96&sortby=7&curpage={page_index}", headers=self.site_headers)
            self.parse_response(url, base_category, response, page_index)

    def parse_response(self, url, base_category, response, page_index=1):
        script_data = response.text.replace("\\", "")
        products = script_data.split("RecommendedListingCollectionItem")
        self.print_out(f"{base_category} : {page_index} : {len(products)} : {url}")

        if len(products) > 10 and len(products) < 200:
            for product in products[1:-1]:
                try:
                    description = product.split('"displayName":"')[1].split('","')[0].replace("u0026", "&")
                    reviews = int(product.split('"totalCount":')[1].split('}')[0])

                    if description == "Our App" or description == "" or description == base_category or reviews < 100 or reviews > 30000:
                        continue
                    
                    product_url = product.split('"listingUrl":"')[1].split('"')[0]
                    if product_url in self.history or "/pdp/" not in product_url:
                        continue

                    product_data = {
                        "Description": description,
                        "URL": product_url,
                        "Price": product.split('"amount":"')[1].split('"')[0],
                        "Reviews": reviews,
                        "Rating": product.split('"averageRating":')[1].split(',')[0],
                        "Category": base_category,
                    }
                    self.write(product_data)
                    self.history.append(product_url)
                    self.counts[base_category] += 1
                    if self.counts[base_category] > self.limit:
                        return
                except:
                    pass
        else:
            script_data = response.text.replace("\\", "").split('"baseURL":"')[-1]
            products = script_data.split(',"url":"')

            self.print_out(f"___ {base_category} : {page_index} : {len(products)} : {url}")

            if len(products) < 10:
                return

            for product in products[1:]:
                try:
                    description = product.split('"product_name":"')[1].split('",')[0].replace("u0026", "&")
                    reviews = int(product.split('"review_count":')[1].split(',')[0])

                    if description == "Our App" or description == "" or description == base_category or reviews < 100:
                        continue
                    
                    product_url = product.split('"')[0]
                    if product_url in self.history or "/pdp/" not in product_url:
                        continue

                    product_data = {
                        "Description": description,
                        "URL": product.split('"')[0],
                        "Price": product.split('"display":{"__typename":"SFPricing_SinglePrice","currency":"USD","label":"NONE","measurement":"REGULAR","value":')[1].split('}')[0],
                        "Reviews": reviews,
                        "Rating": product.split('"average_overall_rating":"')[1].split('"')[0],
                        "Category": base_category,
                    }
                    self.write(product_data)
                    self.history.append(product_url)
                    self.counts[base_category] += 1
                    if self.counts[base_category] > self.limit:
                        return
                except:
                    pass


class OverstockScraper(BaseScraper):
    base_url = "https://www.overstock.com"
    api_url = "https://api.overstock.com/vsearch/products/v1"
    scraper_api = "http://api.scraperapi.com?api_key=&url="
    site_headers = {
        "Accept": "*/*",
        "Content-type": "application/json",
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }
    csv_headers = [
        'Description',
        'URL',
        'Price',
        'Reviews',
        'Rating',
        'Category',
    ]
    counts = {}
    limit = 10000
    history = []
    name = "overstock1"
    default_category = {
        "Sofas": "Sofas",
        "Sectional Sofas": "Sectionals",
        "Benches": "Bedroom Benches",
        # "Ottomans and Poufs": "",
        "Accent Chairs": "Chairs & Seating",
        "Recliner Chairs": "Chairs & Seating",
        "Coffee Tables": "Coffee Tables & End Tables",
        "TV Stands": "TV Stands & Media Storage Furniture",

        "Beds and Headboards": "Beds & Headboards",
        "Bedroom Sets": "Bedroom Sets",
        "Headboards": "Beds & Headboards",
        "Bed Frames": "Beds & Headboards",
        "Dressers": "Dressers & Chests",
        "Nightstands": "Nightstands",
        "Armoires and Wardrobes": "Armoires & Wardrobes",
        "Mattresses": "Mattresses & Foundations",
        "Kids Beds": "Toddler & Kids Bedroom Furniture",

        "Patio Furniture Sets": "Outdoor & Patio Furniture",
        "Outdoor Decor": "Outdoor Decor",
        "Garden": "Garden",
        # "Sports and Fitness": "",
        "Outdoor Shades and Structures": "Outdoor Shades",
        "Outdoor Lighting": "Outdoor Lighting",
    }

    def run(self):
        try:
            self.print_out("\nStarting...")
            response = self.session.get(f"{self.base_url}")
            tree = etree.HTML(response.text)
            sections = tree.xpath("//nav-menu[contains(@class, 'js-mega-nav')]")
            for section_index in [0, 1]:
                categories = sections[section_index].xpath(".//li")
                for category in categories[:-1]:
                    category_name = self.validate(category.xpath(".//text()"))
                    category_url = self.validate(category.xpath(".//a/@href"))
                    if category_name in self.default_category:
                        category_name = self.default_category[category_name]
                        self.parse_page(category_name, category_url)

            for section_index in range(19, 25):
                category = sections[section_index]
                category_name = self.validate(category.xpath(".//div[@class='main-nav__item-content']//text()"))
                category_url = self.validate(category.xpath(".//div[@class='main-nav__item-content']//a/@href"))
                if category_name in self.default_category:
                    category_name = self.default_category[category_name]
                    self.parse_page(category_name, category_url)

        except Exception as e:
            self.print_out(f"run: {e}")

    def parse_page(self, name, url):
        try:
            response = self.session.get(f"{self.base_url}{url}")
            taxonomy_id = response.text.split("'taxonomyId':")[1].split(",")[0].replace('"', '').strip()
            self.print_out(f"parse_page: {name} - {taxonomy_id}")
            if taxonomy_id == "":
                return

            payload = {
                "client":{
                    "id":"ostk",
                    "version":"1.0.0",
                    "deviceType":"DESKTOP"
                },
                "user":{
                    "seed":"3622946904276041631",
                    "language":"en",
                    "country":"US",
                    "currency":"USD",
                    "zip":"",
                    "zipByIp":"",
                    "requestId":""
                },
                "query":{
                    "productSearchQuery":{
                        "taxonomies":[taxonomy_id],
                        "attributes":{},
                        "restrictions":{},
                        "ranges":{},
                        "searchParameters":{
                            "fastshipping":None,
                            "oos":None,
                            "page":1,
                            "sort":"bestselling",
                            "rating":None
                        }
                    },
                    "origin":{
                        "scheme":"https",
                        "hostType":"DomainName",
                        "host":"www.overstock.com"
                    }
                },
                "requires":[
                    "banners",
                    "facets",
                    "meta",
                    "products",
                    "redirect",
                    "relatedSearches",
                    "selectedFacets",
                    "seoMetadata",
                    "sponsoredProducts",
                    "sponsoredShowcase",
                    "sortOptions",
                    "taxonomyFacets",
                    "notating",
                    "featuredProduct"
                ],
                "conversationalSearch":{},
                "clientProfileOverrides":{
                    "productCount":{
                        "rows":81,
                        "maxSponsoredProducts":21
                    },
                    "sponsoredShowcaseProductCount":{
                        "rows":0,
                        "maxSponsoredProducts":0
                    }
                },
                "verboseLogging":False,
                "url":"https://www.overstock.com/collections/sofas"
            }
            self.parse_category(name, payload)
        except Exception as e:
            self.print_out(f"parse_page: {name} - {e}")

    def parse_category(self, name, payload, level="Color"):
        try:
            response = self.session.post(
                self.api_url,
                headers = self.site_headers,
                data = json.dumps(payload)
            ).json()

            self.print_out(f"parse_category: {name} - {level}")
            if level == "Facet":
                self.parse_facet_category(name, payload, response)
            else:
                for facet in response.get("facets"):
                    if facet.get("displayName") == "Color" and level == "Color":
                        for facet_value in facet.get("values", []):
                            if facet_value.get("count") == 0:
                                continue

                            attribute_group_id = facet.get("attributeGroupId")
                            payload["query"]["productSearchQuery"]["attributes"][attribute_group_id] = {
                                "id": attribute_group_id,
                                "values": [facet_value.get("attributeId")]
                            }
                            self.parse_category(name, payload, "Price")

                    if facet.get("displayName") == "Price" and level == "Price":
                        for facet_value in facet.get("values", []):
                            if facet_value.get("count") == 0:
                                continue

                            payload["query"]["productSearchQuery"]["ranges"] = {
                                "price": {
                                    "id": "price",
                                    "min": facet_value.get("min"),
                                    "max": facet_value.get("max")
                                }
                            }
                            self.parse_category(name, payload, "Facet")
        except Exception as e:
            self.print_out(f"parse_category: {name} - {e}")

    def parse_facet_category(self, name, payload, response):
        result_count = response.get("resultCount", 0)
        self.print_out(f"parse_facet_category: {name} - {result_count}")
        if result_count == 0:
            return
        elif result_count < 60:
            self.parse_products(name, response.get("products"))
        else:
            for page_index in range(1, 21):
                try:
                    self.print_out(f"parse_facet_category: {page_index}")
                    payload["query"]["productSearchQuery"]["searchParameters"]["page"] = page_index
                    response = self.session.post(
                        self.api_url,
                        headers = self.site_headers,
                        data = json.dumps(payload)
                    ).json()
                    products = response.get("products")
                    if len(products) == 0:
                        return
                    self.parse_products(name, products)
                except Exception as e:
                    self.print_out(f"parse_facet_category: {name} - {page_index} - {e}")

    def parse_products(self, name, products):
        try:
            product_data = {}
            product_ids = []
            for product in products:
                product_id = self.eliminate_space(self.validate(product.get("url")).split("-"))[-1]
                if product_id in self.history:
                    continue

                product_ids.append(product_id)
                self.history.append(product_id)
                product_data[product_id] = {
                    "Description": self.validate(product.get("title")),
                    "URL": f"{self.base_url}/products/{self.validate(product.get('url'))}",
                    "Price": self.validate(product.get("pricing", {}).get("minPrice")),
                    "Review": 0,
                    "Rating": 0.0,
                    "Category": name,
                }

            review_url = f"https://display.powerreviews.com/m/1280018588/l/en_US/product/{'%2C'.join(product_ids)}/snippet?apikey=0ce15d13-67ca-47dd-8c72-1d5e4694ada3&_noconfig=true"
            review_response = self.session.get(
                review_url, 
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Accept-encoding": "gzip, deflate, br, zstd",
                    "Upgrade-insecure-requests": "1",
                    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
                }
            )
            reviews = review_response.json().get("results")
            for review in reviews:
                product_id = self.validate(review.get("page_id"))
                product_data[product_id]["Reviews"] = self.validate(review.get("rollup", {}).get("review_count"))
                product_data[product_id]["Rating"] = self.validate(review.get("rollup", {}).get("average_rating"))

            for key, value in product_data.items():
                self.write(value)

        except Exception as e:
            self.print_out(f"parse_product: {name} - {e}")


class BedbathandbeyondScraper(BaseScraper):
    base_url = "https://www.bedbathandbeyond.com"
    scraper_api = "http://api.scraperapi.com?api_key=&url="
    site_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Cookie": 'ostk_aggr_year=country^US|currency^USD|language^en|mxcuserseed^4183562443235745007; ostk_aggr_year2=""; ostk_campaign=""; _gcl_au=1.1.1099857975.1724092056; _ga=GA1.1.13332258.1724092057; _tt_enable_cookie=1; _ttp=c0EUmGERZP79s2-Ste3vU2aLcu2; _mibhv=anon-1724092062513-1610773262_9978; _pin_unauth=dWlkPU5qSXlNR0psTmpjdE5EWXlNUzAwWVdZMExXSmtORFV0TldaaFlqSTVaRFl5WW1FMw; salsify_session_id=e50be505-45fe-442c-ac83-713c44addb46; mxcproclicks=33625557|28069572|34665876|37177980|; se_list=se_list^0|4|181|55|; pageTriggers=gdpr^3|triggerFiredTime^1724772314879|gdprExpiration^1731872736135|spinnerLightbox^1|spinnerLightboxExpiration^1724352351315|pushNotifications^1|entryLightbox^1|entryLightboxExpiration^1725031514879; mxclastvisit=20240828; mxcsurftype=4; ab.storage.deviceId.5c2ca4f1-0219-4717-859b-ca7dceb0be43=%7B%22g%22%3A%2201755eb4-9bb4-02c8-a36e-b47302af0874%22%2C%22c%22%3A1724092061534%2C%22l%22%3A1724825005565%7D; mpid=-5819834686019943184; _clck=1whorav%7C2%7Cfop%7C0%7C1692; ostk_aggr_session=sessstrt^1724825002870|billingcountry^US|gcr^false|cart.item-count^0|mxcshopmore^http%3A%2F%2Fwww.bedbathandbeyond.com%2F|dlp^k|postal^33132; sbsd_ss=ab8e18ef4e; sbsd_c=4~1~441805865~pllYCKymKW5kPxU+Obtxn+Ht5G2HBbfq9ZXBzIrg4gdI98wdr3ELW1JhA51n3xz66JzEawBXJChPb9LgYgJUqPjT8yV02GjMHo4TVF7v+S29XCzmEo/CnffaQjHwjE1wnS3xQgTknDE2zVCDO9+os+Bk5FTM7jJ3dZDNVWpERcbJGhvCC5isN1sgT6HYT5BiV6Y9590J0wACQqV2QIcxB0MHYCThfcIjs3DnypOQvX0gU=; _abck=29BD7CDDDFC627E22DB5DDD63E2A136C~0~YAAQWnQyF2Rb2JORAQAA5UgCmAz54HZ2EaJTT5J4qxaTiEPL5y/c/2CtrPV8i6ClqameoPrvqeQqxxZsloKtA4GAsd3MucyWWbnMk4lzkzwkFmSsN+/2qXtsmB3EwrF/62eQdbKrkZVIQyuDPia35Ilp9X8cIOIGg9+qnEn7LmnSpoFmYUwquCHVvWlv6Y50uTbMH+3FVm3a4Dt/TOI2uWcyWv95bEgRrgUIgtO/Tj5o1EHAAhCVweuMStz5EANpRAGDJG0pTp+C1A+5rPujLduJ4eDTMWybt3kxsESgxMGUhAfg+ckXhasPWmKPH1ARrM/X0XrIMnn2nsFClk1Y5sPU4lZ6gDCJbSwS8sVxsyw96rxKzGzMuWEXo/5fozh/YGA6RxLTqlxV9TKOpW5jOUi/C5dVcUPL0uNddXltQjBNrw==~-1~-1~1724835772; AKA_A2=A; sbsd_o=4C99E16079421EB5BAC227F97B7A1C4FBFC3D1F57101978EBE8A0627374F2CAE~syi4YpM/GLfqntkAcL8wS7ZwYGODxRN2CI/1V6oO8I6wPlNBSuSzUBUaP7RyU8VUM8CZ4ZgwNZ6bK7QRV9xLD7up6UdBAZAhTMz6N1y4CDjqDJvtwJtiTNgRNtXlYOuNhseEZDyuW4Q6UHS4yya3rwJXcq4fnKAT7rlWxiHzbEzjob49wrv4Qa4OHbHPEXwjHXDJduidT8i4vTRzT8csE5XZfznXdBol6yy+F7N/d8bfjxqezdZQ8LXb26dAK5hxQ+2GgSHPDhn88LMhWB057iLP9gqi42tPH/cEN+IcjmZZkUwMXjoy82++1zgrJIRJasWB/nMWK70EPlQoclmzw5tQGkhSV63FCXGJmtg1rMUs=; sbsd=slaaOP+7bl2BarblWToa3Dom3P62U8NkUZcQDEnfCd9waEwyeQu3/7nrWAq8vk6ovOv6gvnk/C8ieiQ8R/W0tJ1r8uyXDhoUA8iyQggs9auh4mitd3KpO1wZioq1C30Bz/MnFA9Oon+s4Iq0rBUHQCfv/hXf6vfhRMG/kdCsl6dEubbQX0BTglZChBSLDCW/7; bm_sz=1053F32B3AE706BDF6223F5AFCD4260B~YAAQWnQyF/xr2JORAQAAeJYEmBgr8Ri00ZqBvI0hhEoHPhAD/+pzSwkCcoIhPdgJWp3Hxd+GkpuDaYqwcx+HvBsZUKhKYl60oRj24tcFNijbripIyjQt8TxO3VQA1AVfOSSF4IE1XdvKzf21FrsxWLbIj3x0AmzX1OgWXxq3d8f0vKIOVCeCWBUwtLB8EJZpljPgbI9Yj2Gw22CqeEXHTwwhz2KSHqHc4hmdK6S5GPZIseXWJeY7rG/BEsjecDpjjsbyKpCIrfaFbZCmNINpdswXHlB8JJevloybr+EzF7WBgXfgawXDmwVrnqSKsdkk2STHwyfyHnflc2lYrL1xdGrjXFryW4nn9OYu5X9MIawAwEp3efmuKv68HN3ioo5E9S3bky9fMMJT3X6jIunp8VL8uZotXTHhMgzcZKMuCu2OmIwcfSRUUmww//Hnzvuh/s7vg8/sLHM7uHHjmtxycMTS6Ac6aPK1NUu4hkthxrfkfN9mzpNb5IJvhFf5tQxCbZ/YGOZvrTQBdnAr+MLYnsC0/Q+cTSIwDzsGVehy3WpXE5kTwl0fIWQ/~4277825~3552070; _ga_8MPQ3CZZFH=GS1.1.1724825003.3.1.1724832322.60.0.0; ak_bmsc=620C6BA8E7BACA5913EDCFF148E2FFEA~000000000000000000000000000000~YAAQWnQyFz9s2JORAQAAVpwEmBhdtyHKGfeYmCxMc9ZoJs3x+eW3TCgx7rAEm0mfr8PjrhAqwDRAySY4N2PgrUo9WraBxAw824Cs/zWmxmxWdoPERGc+kqavFBif4vj3qzIpQvus684ljbjvZqi+PTk3avkxfywQdAz1LoAmtnERctNyI6h0A8GZYRJbjCoWtJ59piZTXH14ygjLv2W6Vcole58RViFUg1Ime7iOBvTW7kraWAa897Bug0QtRsrTBf1FWfU9JT2EFUqFYjuXcwwTrstb4LZCzu23VZcJULGLRWYjEamAAo5tT8oMH8LaD26a4Wv94QD9mKW1xPUL7OB7aZGIL/LpP5CABhYK2K1yTcK1FeKk8h7oglW9M19uEsGvQMxZMkundgfUDBTBWpOr0FgjaPp2bYbk+zqhNe4PoApgawPs2Rq+neuxQ+aVRugC5BafaaOa0cdZxk+hIQRwKLfz; _uetsid=905849c0648811efa690991e2afa49d4; _uetvid=b87332f05e5811ef9e820179e3af739a; ab.storage.sessionId.5c2ca4f1-0219-4717-859b-ca7dceb0be43=%7B%22g%22%3A%22d92d0320-194b-97e4-ebe5-10572aad27b0%22%2C%22e%22%3A1724834124004%2C%22c%22%3A1724825005564%2C%22l%22%3A1724832324004%7D; bm_lso=4C99E16079421EB5BAC227F97B7A1C4FBFC3D1F57101978EBE8A0627374F2CAE~syi4YpM/GLfqntkAcL8wS7ZwYGODxRN2CI/1V6oO8I6wPlNBSuSzUBUaP7RyU8VUM8CZ4ZgwNZ6bK7QRV9xLD7up6UdBAZAhTMz6N1y4CDjqDJvtwJtiTNgRNtXlYOuNhseEZDyuW4Q6UHS4yya3rwJXcq4fnKAT7rlWxiHzbEzjob49wrv4Qa4OHbHPEXwjHXDJduidT8i4vTRzT8csE5XZfznXdBol6yy+F7N/d8bfjxqezdZQ8LXb26dAK5hxQ+2GgSHPDhn88LMhWB057iLP9gqi42tPH/cEN+IcjmZZkUwMXjoy82++1zgrJIRJasWB/nMWK70EPlQoclmzw5tQGkhSV63FCXGJmtg1rMUs=^1724832324197; cto_bundle=78rsUF9jQjNDRnJQT29reFElMkZldmJ6eWk2UiUyQnJQVUU3bWRtUGc0MEIwb3NGRWtnenBmeFFFTjRhdzdiJTJGVFQzamVtbk45WWIlMkZUODlTeTB0MHZUYlhGbVk4QlROSVJ0ZDZlR2V6SHRNZGNndnpSJTJCbnQ5NnBYaCUyQlljbDI4SThGZHElMkZEMVR0ZTIwa2UxMnBDRlg1SFl2T1VaYlNudEI5NUl5dUZtT1d4bmE3MlgwM1VSSSUzRA; _clsk=zvitrb%7C1724832325307%7C36%7C0%7Cx.clarity.ms%2Fcollect; utag_main=v_id:01916be5136b001d5b8ffaf038a20506f002106700bd0$_sn:3$_se:389$_ss:0$_st:1724834126553$dc_visit:3$ses_id:1724825004735%3Bexp-session$_pn:24%3Bexp-session$dc_event:41%3Bexp-session$dc_region:us-east-1%3Bexp-session',
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }
    api_url = "https://api.bedbathandbeyond.com/kronos/spa"
    api_headers = {
        "Accept": "*/*",
        "Accept-encoding": "gzip, deflate, br, zstd",
        "Accept-language": "en-US,en;q=0.9",
        "Client-id": "hyperion",
        "Cookie": 'ostk_aggr_year=country^US|currency^USD|language^en|mxcuserseed^4183562443235745007; ostk_aggr_year2=""; ostk_campaign=""; _gcl_au=1.1.1099857975.1724092056; _ga=GA1.1.13332258.1724092057; _tt_enable_cookie=1; _ttp=c0EUmGERZP79s2-Ste3vU2aLcu2; _mibhv=anon-1724092062513-1610773262_9978; _pin_unauth=dWlkPU5qSXlNR0psTmpjdE5EWXlNUzAwWVdZMExXSmtORFV0TldaaFlqSTVaRFl5WW1FMw; salsify_session_id=e50be505-45fe-442c-ac83-713c44addb46; mxcproclicks=33625557|28069572|34665876|37177980|; se_list=se_list^0|4|181|55|; pageTriggers=gdpr^3|triggerFiredTime^1724772314879|gdprExpiration^1731872736135|spinnerLightbox^1|spinnerLightboxExpiration^1724352351315|pushNotifications^1|entryLightbox^1|entryLightboxExpiration^1725031514879; mxclastvisit=20240828; mxcsurftype=4; ab.storage.deviceId.5c2ca4f1-0219-4717-859b-ca7dceb0be43=%7B%22g%22%3A%2201755eb4-9bb4-02c8-a36e-b47302af0874%22%2C%22c%22%3A1724092061534%2C%22l%22%3A1724825005565%7D; mpid=-5819834686019943184; _clck=1whorav%7C2%7Cfop%7C0%7C1692; ostk_aggr_session=sessstrt^1724825002870|billingcountry^US|gcr^false|cart.item-count^0|mxcshopmore^http%3A%2F%2Fwww.bedbathandbeyond.com%2F|dlp^k|postal^33132; sbsd_ss=ab8e18ef4e; sbsd_c=4~1~441805865~pllYCKymKW5kPxU+Obtxn+Ht5G2HBbfq9ZXBzIrg4gdI98wdr3ELW1JhA51n3xz66JzEawBXJChPb9LgYgJUqPjT8yV02GjMHo4TVF7v+S29XCzmEo/CnffaQjHwjE1wnS3xQgTknDE2zVCDO9+os+Bk5FTM7jJ3dZDNVWpERcbJGhvCC5isN1sgT6HYT5BiV6Y9590J0wACQqV2QIcxB0MHYCThfcIjs3DnypOQvX0gU=; _abck=29BD7CDDDFC627E22DB5DDD63E2A136C~0~YAAQWnQyF2Rb2JORAQAA5UgCmAz54HZ2EaJTT5J4qxaTiEPL5y/c/2CtrPV8i6ClqameoPrvqeQqxxZsloKtA4GAsd3MucyWWbnMk4lzkzwkFmSsN+/2qXtsmB3EwrF/62eQdbKrkZVIQyuDPia35Ilp9X8cIOIGg9+qnEn7LmnSpoFmYUwquCHVvWlv6Y50uTbMH+3FVm3a4Dt/TOI2uWcyWv95bEgRrgUIgtO/Tj5o1EHAAhCVweuMStz5EANpRAGDJG0pTp+C1A+5rPujLduJ4eDTMWybt3kxsESgxMGUhAfg+ckXhasPWmKPH1ARrM/X0XrIMnn2nsFClk1Y5sPU4lZ6gDCJbSwS8sVxsyw96rxKzGzMuWEXo/5fozh/YGA6RxLTqlxV9TKOpW5jOUi/C5dVcUPL0uNddXltQjBNrw==~-1~-1~1724835772; AKA_A2=A; sbsd_o=4C99E16079421EB5BAC227F97B7A1C4FBFC3D1F57101978EBE8A0627374F2CAE~syi4YpM/GLfqntkAcL8wS7ZwYGODxRN2CI/1V6oO8I6wPlNBSuSzUBUaP7RyU8VUM8CZ4ZgwNZ6bK7QRV9xLD7up6UdBAZAhTMz6N1y4CDjqDJvtwJtiTNgRNtXlYOuNhseEZDyuW4Q6UHS4yya3rwJXcq4fnKAT7rlWxiHzbEzjob49wrv4Qa4OHbHPEXwjHXDJduidT8i4vTRzT8csE5XZfznXdBol6yy+F7N/d8bfjxqezdZQ8LXb26dAK5hxQ+2GgSHPDhn88LMhWB057iLP9gqi42tPH/cEN+IcjmZZkUwMXjoy82++1zgrJIRJasWB/nMWK70EPlQoclmzw5tQGkhSV63FCXGJmtg1rMUs=; sbsd=slaaOP+7bl2BarblWToa3Dom3P62U8NkUZcQDEnfCd9waEwyeQu3/7nrWAq8vk6ovOv6gvnk/C8ieiQ8R/W0tJ1r8uyXDhoUA8iyQggs9auh4mitd3KpO1wZioq1C30Bz/MnFA9Oon+s4Iq0rBUHQCfv/hXf6vfhRMG/kdCsl6dEubbQX0BTglZChBSLDCW/7; bm_sz=1053F32B3AE706BDF6223F5AFCD4260B~YAAQWnQyF/xr2JORAQAAeJYEmBgr8Ri00ZqBvI0hhEoHPhAD/+pzSwkCcoIhPdgJWp3Hxd+GkpuDaYqwcx+HvBsZUKhKYl60oRj24tcFNijbripIyjQt8TxO3VQA1AVfOSSF4IE1XdvKzf21FrsxWLbIj3x0AmzX1OgWXxq3d8f0vKIOVCeCWBUwtLB8EJZpljPgbI9Yj2Gw22CqeEXHTwwhz2KSHqHc4hmdK6S5GPZIseXWJeY7rG/BEsjecDpjjsbyKpCIrfaFbZCmNINpdswXHlB8JJevloybr+EzF7WBgXfgawXDmwVrnqSKsdkk2STHwyfyHnflc2lYrL1xdGrjXFryW4nn9OYu5X9MIawAwEp3efmuKv68HN3ioo5E9S3bky9fMMJT3X6jIunp8VL8uZotXTHhMgzcZKMuCu2OmIwcfSRUUmww//Hnzvuh/s7vg8/sLHM7uHHjmtxycMTS6Ac6aPK1NUu4hkthxrfkfN9mzpNb5IJvhFf5tQxCbZ/YGOZvrTQBdnAr+MLYnsC0/Q+cTSIwDzsGVehy3WpXE5kTwl0fIWQ/~4277825~3552070; _ga_8MPQ3CZZFH=GS1.1.1724825003.3.1.1724832322.60.0.0; ak_bmsc=620C6BA8E7BACA5913EDCFF148E2FFEA~000000000000000000000000000000~YAAQWnQyFz9s2JORAQAAVpwEmBhdtyHKGfeYmCxMc9ZoJs3x+eW3TCgx7rAEm0mfr8PjrhAqwDRAySY4N2PgrUo9WraBxAw824Cs/zWmxmxWdoPERGc+kqavFBif4vj3qzIpQvus684ljbjvZqi+PTk3avkxfywQdAz1LoAmtnERctNyI6h0A8GZYRJbjCoWtJ59piZTXH14ygjLv2W6Vcole58RViFUg1Ime7iOBvTW7kraWAa897Bug0QtRsrTBf1FWfU9JT2EFUqFYjuXcwwTrstb4LZCzu23VZcJULGLRWYjEamAAo5tT8oMH8LaD26a4Wv94QD9mKW1xPUL7OB7aZGIL/LpP5CABhYK2K1yTcK1FeKk8h7oglW9M19uEsGvQMxZMkundgfUDBTBWpOr0FgjaPp2bYbk+zqhNe4PoApgawPs2Rq+neuxQ+aVRugC5BafaaOa0cdZxk+hIQRwKLfz; _uetsid=905849c0648811efa690991e2afa49d4; _uetvid=b87332f05e5811ef9e820179e3af739a; ab.storage.sessionId.5c2ca4f1-0219-4717-859b-ca7dceb0be43=%7B%22g%22%3A%22d92d0320-194b-97e4-ebe5-10572aad27b0%22%2C%22e%22%3A1724834124004%2C%22c%22%3A1724825005564%2C%22l%22%3A1724832324004%7D; bm_lso=4C99E16079421EB5BAC227F97B7A1C4FBFC3D1F57101978EBE8A0627374F2CAE~syi4YpM/GLfqntkAcL8wS7ZwYGODxRN2CI/1V6oO8I6wPlNBSuSzUBUaP7RyU8VUM8CZ4ZgwNZ6bK7QRV9xLD7up6UdBAZAhTMz6N1y4CDjqDJvtwJtiTNgRNtXlYOuNhseEZDyuW4Q6UHS4yya3rwJXcq4fnKAT7rlWxiHzbEzjob49wrv4Qa4OHbHPEXwjHXDJduidT8i4vTRzT8csE5XZfznXdBol6yy+F7N/d8bfjxqezdZQ8LXb26dAK5hxQ+2GgSHPDhn88LMhWB057iLP9gqi42tPH/cEN+IcjmZZkUwMXjoy82++1zgrJIRJasWB/nMWK70EPlQoclmzw5tQGkhSV63FCXGJmtg1rMUs=^1724832324197; cto_bundle=78rsUF9jQjNDRnJQT29reFElMkZldmJ6eWk2UiUyQnJQVUU3bWRtUGc0MEIwb3NGRWtnenBmeFFFTjRhdzdiJTJGVFQzamVtbk45WWIlMkZUODlTeTB0MHZUYlhGbVk4QlROSVJ0ZDZlR2V6SHRNZGNndnpSJTJCbnQ5NnBYaCUyQlljbDI4SThGZHElMkZEMVR0ZTIwa2UxMnBDRlg1SFl2T1VaYlNudEI5NUl5dUZtT1d4bmE3MlgwM1VSSSUzRA; _clsk=zvitrb%7C1724832325307%7C36%7C0%7Cx.clarity.ms%2Fcollect; utag_main=v_id:01916be5136b001d5b8ffaf038a20506f002106700bd0$_sn:3$_se:389$_ss:0$_st:1724834126553$dc_visit:3$ses_id:1724825004735%3Bexp-session$_pn:24%3Bexp-session$dc_event:41%3Bexp-session$dc_region:us-east-1%3Bexp-session',
        "Request-url": "https://www.bedbathandbeyond.com",
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }
    csv_headers = [
        'Description',
        'URL',
        'Price',
        'Reviews',
        'Rating',
        'Category',
    ]
    counts = {}
    limit = 10000
    history = []
    name = "bedbath"
    default_category = {
        "Sofas and Couches": "Sofas",
        "Sectionals": "Sectionals",
        "Benches": "Bedroom Benches",
        "Ottomans and Poufs": "Ottomans & Poufs",
        "Accent Chairs": "Chairs & Seating",
        "Recliners": "Chairs & Seating",
        "Coffee and Accent Tables": "Coffee Tables & End Tables",
        "TV Stands": "TV Stands & Media Storage Furniture",
        # "Best Sellers": "",

        "Beds": "Beds & Headboards",
        "Bedroom Sets": "Bedroom Sets",
        "Headboards": "Beds & Headboards",
        "Bed Frames": "Beds & Headboards",
        "Dressers and Chests": "Dressers & Chests",
        "Nightstands": "Nightstands",
        "Armoires and Wardrobes": "Armoires & Wardrobes",
        "Mattresses": "Mattresses & Foundations",
        "Kids Beds": "Toddler & Kids Bedroom Furniture",

        "Patio Furniture": "Outdoor & Patio Furniture",
        "Outdoor Decor": "Outdoor Decor",
        "Outdoor Shades and Structures": "Outdoor Shades",
        "Garden": "Garden",
        "Grills and Outdoor Cooking": "Grills & Outdoor Cooking",
        # "Sports and Outdoors": "",
    }

    def run(self):
        try:
            self.print_out("\nStarting...")
            response = self.session.get(f"{self.base_url}", headers=self.site_headers)
            tree = etree.HTML(response.text)
            sections = tree.xpath("//div[@class='swh_DropDown_column']")

            for section_index in [0, 1]:
                categories = sections[section_index].xpath(".//a[@class='swh_DropDown_columnLink']")
                for category in categories:
                    category_name = self.validate(category.xpath(".//text()"))
                    category_url = self.base_url + self.validate(category.xpath("./@href"))
                    if category_name in self.default_category:
                        category_name = self.default_category[category_name]
                        self.parse_category(category_name, category_url)

            for section_index in range(42, 48):
                category = sections[section_index]
                category_name = self.validate(category.xpath(".//a[@class='swh_DropDown_columnLink swh_DropDown_columnTitle']//text()"))
                category_url = self.base_url + self.validate(category.xpath(".//a[@class='swh_DropDown_columnLink swh_DropDown_columnTitle']/@href"))
                if category_name in self.default_category:
                    category_name = self.default_category[category_name]
                    self.parse_category(category_name, category_url)

        except Exception as e:
            self.print_out(f"run: {e}")

    def parse_category(self, name, url, level="Color"):
        try:
            self.api_headers["request-url"] = url
            response = self.session.get(
                self.api_url,
                headers = self.api_headers
            ).json()

            self.print_out(f"parse_category: {name} - {level}")
            if level == "Facet":
                self.parse_facet_category(name, url, response)
            else:
                for facet in response.get("pageData", {}).get("facets", []):
                    if facet.get("displayName") == "Color" and level == "Color":
                        for facet_value in facet.get("values", []):
                            if facet_value.get("count") == 0:
                                continue

                            self.parse_category(
                                name,
                                f"{url}&a{facet.get('attributeGroupId')}={facet_value.get('attributeId')}",
                                "Price"
                            )

                    if facet.get("displayName") == "Price" and level == "Price":
                        for facet_value in facet.get("values", []):
                            if facet_value.get("count") == 0:
                                continue

                            self.parse_category(
                                name,
                                f"{url}&price={facet_value.get('min')}:{facet_value.get('max')}",
                                "Facet"
                            )
        except Exception as e:
            self.print_out(f"parse_category: {name} - {e}")

    def parse_facet_category(self, name, url, response):
        result_count = response.get("pageData", {}).get("resultCount", 0)
        self.print_out(f"parse_facet_category: {name} - {result_count} - {url}")
        if result_count == 0:
            return
        elif result_count < 64:
            self.parse_products(name, response.get("products"))
        else:
            for page_index in range(1, 85):
                try:
                    self.api_headers["request-url"] = f"{url}&page={page_index}"
                    response = self.session.get(
                        self.api_url,
                        headers = self.api_headers
                    ).json()
                    products = response.get("pageData", {}).get("products", [])
                    self.print_out(f"parse_facet_category: {name} - {page_index} - {len(products)}")
                    if len(products) == 0:
                        return
                    self.parse_products(name, products)
                except Exception as e:
                    self.print_out(f"parse_facet_category: {name} - {page_index}")
                    return

    def parse_products(self, name, products):
        for product in products:
            try:
                product_id = self.validate(product.get("id"))
                review_count = int(self.validate(product.get("reviews", {}).get("count", 0)))
                if product_id in self.history or review_count == 0:
                    continue

                self.history.append(product_id)
                data = {
                    "Description": self.validate(product.get("name")),
                    "URL": self.validate(product.get("urls", {}).get("productPage")),
                    "Price": self.validate(product.get("pricing", {}).get("base", {}).get("price")).replace("$", ""),
                    "Reviews": review_count,
                    "Rating": self.validate(product.get("reviews", {}).get("rating", 0)),
                    "Category": name,
                }
                self.write(data)

            except Exception as e:
                self.print_out(f"parse_product: {name} - {e}")


if __name__ == '__main__':
    BedbathandbeyondScraper().run()
