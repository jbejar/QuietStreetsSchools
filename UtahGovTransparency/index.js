var request = require("request");
sum = 0;
ids = ["-1","","219","855","259","1201","999","221","223","867","1009","1119","1203","833","25","283","1598","41","151","205","853","225","45","1631","47","1599","227","107","49","153","207","1001","229","39","173","191","37","51","849","43","1003","231","193","1205","233","53","235","109","289","55","57","1133","111","175","875","1632","237","59","113","179","239","35","61","1005","63","115","241","1600","985","243","245","195","209","1121","977","863","247","67","1149","27","69","177","1007","197","71","163","73","165","167","75","169","77","199","201","79","171","119","869","65","81","121","975","83","871","249","261","181","123","251","1619","125","85","127","1123","129","203","31","133","281","1011","29","131","89","91","253","1207","135","139","291","183","1117","1015","185","141","93","95","1618","255","877","97","1113","865","143","979","997","145","873","1125","187","257","981","147","1209","189","101","1211","263","103","105","1596","287"]
leas = [{"key":"219","value":"Academy for Math Engineering and Science"},{"key":"855","value":"Alianza Academy (CLOSED)"},{"key":"259","value":"Alpine School District"},{"key":"1201","value":"American Academy of Innovation"},{"key":"999","value":"American International School of Utah"},{"key":"221","value":"American Leadership Academy"},{"key":"223","value":"American Preparatory Academy"},{"key":"867","value":"Aristotle Academy (CLOSED)"},{"key":"1009","value":"Ascent Academies of Utah"},{"key":"1119","value":"Athenian eAcademy"},{"key":"1203","value":"Athlos Academy of Utah"},{"key":"833","value":"Bear River Charter School"},{"key":"25","value":"Beaver School District"},{"key":"283","value":"Beehive Science & Technology Academy"},{"key":"1598","value":"Bonneville Academy"},{"key":"41","value":"Box Elder School District"},{"key":"151","value":"C S Lewis Academy"},{"key":"205","value":"Cache County School District"},{"key":"853","value":"Canyon Grove Academy"},{"key":"225","value":"Canyon Rim Academy"},{"key":"45","value":"Canyons School District"},{"key":"1631","value":"Capstone Classical Academy"},{"key":"47","value":"Carbon School District"},{"key":"1599","value":"Center for Creativity Innovation and Discovery"},{"key":"227","value":"Channing Hall Center"},{"key":"107","value":"City Academy"},{"key":"49","value":"Daggett School District"},{"key":"153","value":"DaVinci Academy of Science and the Arts"},{"key":"207","value":"Davis School District"},{"key":"1001","value":"Dixie Montessori Academy"},{"key":"229","value":"Dual Immersion Academy"},{"key":"39","value":"Duchesne School District"},{"key":"173","value":"Early Light Academy"},{"key":"191","value":"East Hollywood High School"},{"key":"37","value":"Edith Bowen Laboratory School"},{"key":"51","value":"Emery School District"},{"key":"849","value":"Endeavor Hall"},{"key":"43","value":"Entheos Academy"},{"key":"1003","value":"Esperanza Elementary"},{"key":"231","value":"Excelsior Academy"},{"key":"193","value":"Fast Forward High School"},{"key":"1205","value":"Franklin Discovery Academy"},{"key":"233","value":"Freedom Academy"},{"key":"53","value":"Garfield School District"},{"key":"235","value":"Gateway Prepatory Academy"},{"key":"109","value":"George Washington Academy"},{"key":"289","value":"Good Foundations Academy"},{"key":"55","value":"Grand School District"},{"key":"57","value":"Granite School District"},{"key":"1133","value":"Greenwood Charter School"},{"key":"111","value":"Guadalupe Charter School"},{"key":"175","value":"Hawthorn Academy"},{"key":"875","value":"Highmark Charter School"},{"key":"1632","value":"Ignite Entrepreneurship Academy"},{"key":"237","value":"InTech Collegiate High School"},{"key":"59","value":"Iron County School District"},{"key":"113","value":"Itineris Early College High School"},{"key":"179","value":"Jefferson Academy"},{"key":"239","value":"John Hancock Charter School"},{"key":"35","value":"Jordan School District"},{"key":"61","value":"Juab School District"},{"key":"1005","value":"Kairos Academy (CLOSED)"},{"key":"63","value":"Kane School District"},{"key":"115","value":"Karl G. Maeser Preparatory Academy"},{"key":"241","value":"Lakeview Academy"},{"key":"1600","value":"Leadership Academy of Utah"},{"key":"985","value":"Leadership Learning Academy"},{"key":"243","value":"Legacy Preparatory Academy"},{"key":"245","value":"Liberty Academy (CLOSED)"},{"key":"195","value":"Lincoln Academy"},{"key":"209","value":"Logan School District"},{"key":"1121","value":"Lumen Scholar Institute"},{"key":"977","value":"MANA Academy"},{"key":"863","value":"Maria Montessori Academy"},{"key":"247","value":"Merit College Preparatory Academy"},{"key":"67","value":"Millard School District"},{"key":"1149","value":"Moab Charter School"},{"key":"27","value":"Monticello Academy"},{"key":"69","value":"Morgan School District"},{"key":"177","value":"Mountain Heights Academy"},{"key":"1007","value":"Mountain West Montessori Academy"},{"key":"197","value":"Mountainville Academy"},{"key":"71","value":"Murray School District"},{"key":"163","value":"Navigator Pointe Academy"},{"key":"73","value":"Nebo School District"},{"key":"165","value":"Noah Webster Academy"},{"key":"167","value":"North Davis Preparatory Academy"},{"key":"75","value":"North Sanpete School District"},{"key":"169","value":"North Star Academy"},{"key":"77","value":"North Summit School District"},{"key":"199","value":"North Utah Academy for Math, Engineering & Science"},{"key":"201","value":"Odyssey Charter School"},{"key":"79","value":"Ogden City School District"},{"key":"171","value":"Ogden Preparatory Academy"},{"key":"119","value":"Open Classroom Charter School"},{"key":"869","value":"Pacific Heritage Academy"},{"key":"65","value":"Paradigm High School of Utah"},{"key":"81","value":"Park City School District"},{"key":"121","value":"Pinnacle Canyon Academy"},{"key":"975","value":"Pioneer High School for the Performing Arts(Closed"},{"key":"83","value":"Piute School District"},{"key":"871","value":"Promontory School of Expeditionary Learning"},{"key":"249","value":"Providence Hall"},{"key":"261","value":"Provo School District"},{"key":"181","value":"Quest Academy"},{"key":"123","value":"Ranches Academy"},{"key":"251","value":"Reagan Academy"},{"key":"1619","value":"Real Salt Lake Academy High School"},{"key":"125","value":"Renaissance Academy"},{"key":"85","value":"Rich School District"},{"key":"127","value":"Rockwell Charter High School"},{"key":"1123","value":"Roots Charter High School"},{"key":"129","value":"Salt Lake Arts Academy"},{"key":"203","value":"Salt Lake Center for Science Education"},{"key":"31","value":"Salt Lake School District"},{"key":"133","value":"Salt Lake School for the Performing Arts"},{"key":"281","value":"San Juan School District"},{"key":"1011","value":"Scholar Academy"},{"key":"29","value":"Sevier School District"},{"key":"131","value":"Soldier Hollow Charter School"},{"key":"89","value":"South Sanpete School District"},{"key":"91","value":"South Summit School District"},{"key":"253","value":"Spectrum Academy"},{"key":"1207","value":"St. George Academy"},{"key":"135","value":"Success Academy"},{"key":"139","value":"Summit Academy"},{"key":"291","value":"Summit Academy High School"},{"key":"183","value":"Syracuse Arts Academy"},{"key":"1117","value":"Terra Academy"},{"key":"1015","value":"The Winter Sports School in Park City"},{"key":"185","value":"Thomas Edison Charter School-North"},{"key":"141","value":"Timpanogos Academy"},{"key":"93","value":"Tintic School District"},{"key":"95","value":"Tooele County School District"},{"key":"1618","value":"Treeside Charter School"},{"key":"255","value":"Tuacahn High School for the Performing Arts"},{"key":"877","value":"Uintah River High School"},{"key":"97","value":"Uintah School District"},{"key":"1113","value":"Utah Career Path High School"},{"key":"865","value":"Utah Connections Academy"},{"key":"143","value":"Utah County Academy of Sciences"},{"key":"979","value":"Utah International Charter School"},{"key":"997","value":"Utah Military Academy"},{"key":"145","value":"Utah Virtual Academy"},{"key":"873","value":"Valley Academy"},{"key":"1125","value":"Vanguard Academy"},{"key":"187","value":"Venture Academy"},{"key":"257","value":"Vista at Entrada, School of Performing Arts & Tech"},{"key":"981","value":"Voyage Academy"},{"key":"147","value":"Walden School of Liberal Arts"},{"key":"1209","value":"Wallace Stegner Academy"},{"key":"189","value":"Wasatch Peak Academy"},{"key":"101","value":"Wasatch School District"},{"key":"1211","value":"Wasatch Waldorf Charter School"},{"key":"263","value":"Washington County School District"},{"key":"103","value":"Wayne School District"},{"key":"105","value":"Weber School District"},{"key":"1596","value":"Weber State University Charter Academy"},{"key":"287","value":"Weilenmann School of Discovery"}]

function searchAllLEAsForVendor(vendor, fiscalYear) {
    if(ids.length <= 0) {
        console.log("Total: " + sum);
        return;
    }
    searchLEAForVendor(leas.pop(), vendor, fiscalYear, () => {
        searchAllLEAsForVendor(vendor);
    });
    
}
function searchLEAForVendor(lea, vendor, fiscalYear, callback) {
    var options = { method: 'GET',
    url: 'https://www.utah.gov/transparency-data/summaryData.rest',
    qs: 
     { govLevel: 'K12+EDUCATION',
       entityId: lea.key,
       transType: '1',
       fiscalYear: fiscalYear + "",
       startsWith: 'false',
       showProgram: 'true',
       showFunction: 'true',
       nodeNum: '0',
       searchType: 'PAYEE',
       vendorName: vendor },
    headers: 
     { 'cache-control': 'no-cache',
       Host: 'www.utah.gov',
       'Postman-Token': 'cc6873db-4531-4b93-94aa-b4ac0ca50a32,d3b98c6d-2f52-4d81-a2a5-43247acffa49',
       'Cache-Control': 'no-cache',
       Connection: 'keep-alive',
       'X-Requested-With': 'XMLHttpRequest',
       Referer: 'https://www.utah.gov/transparency/app.html?govLevel=K12+EDUCATION&entityId=997&fiscalYear=2018&transType=1&title1=K-12+Education%3A+2018%3A+Expense&title2=Utah+Military+Academy&title3=K-12+Education%3A+Utah+Military+Academy%3A+2018%3A+Expense',
       Accept: 'application/json, text/javascript, */*; q=0.01',
       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
       'Accept-Language': 'en-US,en;q=0.9,es-419;q=0.8,es;q=0.7',
       'Accept-Encoding': 'gzip, deflate, br',
       Cookie: 'JSESSIONID=8e31018709dd041688e3d36fe57b; amlbcookie=01; AMSession=_p6JygY0hCvmMoUlp7ipH9Znq2U.*AAJTSQACMDIAAlNLABxXN0FrYkg5ZG1qay9jZmdlT2RSam5XWHVDbHc9AAR0eXBlAANDVFMAAlMxAAIwMQ..*,JSESSIONID=8e31018709dd041688e3d36fe57b; amlbcookie=01; AMSession=_p6JygY0hCvmMoUlp7ipH9Znq2U.*AAJTSQACMDIAAlNLABxXN0FrYkg5ZG1qay9jZmdlT2RSam5XWHVDbHc9AAR0eXBlAANDVFMAAlMxAAIwMQ..*; JSESSIONID=29e114420e72d75b07424c2bff84' } };
  
  request(options, function (error, response, body) {
    if (error) throw new Error(error);
    
    var results = JSON.parse(body).results;
    if(results && results.length > 0) {   
        console.log(lea.value + "\t" + vendor + "\t" + results[0].amount);
        sum += results[0].amount
    } else {
        console.log(lea)
    }
    if(callback) {
        callback();
    }
    
  });
}

searchAllLEAsForVendor('H-Wire', 2018);
