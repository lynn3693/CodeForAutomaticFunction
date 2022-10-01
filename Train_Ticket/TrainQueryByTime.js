require('dotenv').config(); //載入.env環境檔
// 取出.env檔案填寫的FB資訊
const user_StartStation = process.env.StartStation_Setting;
const user_TargetStation = process.env.TargetStation_Setting;
const user_Time = process.env.Timeing_Setting;


const webdriver = require('selenium-webdriver'), // 加入虛擬網頁套件
  By = webdriver.By, // 你想要透過什麼方式來抓取元件，通常使用xpath、css
  until = webdriver.until; // 直到抓到元件才進入下一步(可設定等待時間)
const chrome = require('selenium-webdriver/chrome');
const options = new chrome.Options();
options.addArguments('--log-level=3'); // 這個option可以讓你跟網頁端的console.log說掰掰
// 因為notifications會干擾到爬蟲，所以要先把它關閉
options.setUserPreferences({ 'profile.default_content_setting_values.notifications': 1 });


async function QueryByTime () {
  
  // 建立這個browser的類型
  let driver = await new webdriver.Builder().forBrowser("chrome").withCapabilities(options).build(); // 建立這個Browser的類型
  const web = 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime';//填寫你想要前往的網站 - 台鐵時刻表
  await driver.get(web); // 透過這個driver打開網頁,在這裡要用await確保打開完網頁後才能繼續動作

   // 填入FB登入資訊
   const StartStation = await driver.wait(until.elementLocated(By.xpath('//*[@id="startStation"]'))); // 找出填寫位置
   StartStation.sendKeys(user_StartStation); // 將使用者的資訊填入
   const TargetStation = await driver.wait(until.elementLocated(By.xpath('//*[@id="endStation"]')));// 找出填寫位置
   TargetStation.sendKeys(user_TargetStation);
   const RideDate = await driver.wait(until.elementLocated(By.xpath('//*[@id="rideDate"]')));// 找出填寫位置
   RideDate.sendKeys(user_Time);
 
   // 抓到登入按鈕然後點擊
   const Query = await driver.wait(until.elementLocated(By.xpath('//*[@id="queryForm"]/div[1]/div[3]/div[2]/input')));
   Query.click();
}
QueryByTime(); // 查詢時刻表