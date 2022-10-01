require('dotenv').config(); //載入.env環境檔
// 取出.env檔案填寫的資訊
const user_StartStation = process.env.StartStation_Setting;
const user_TargetStation = process.env.TargetStation_Setting;
const user_Id = process.env.User_Info;
const user_TrainNumber = process.env.Train_No;
const user_Time = process.env.Timeing_Setting;
const CAPTCHA_Key = process.env.CAPTCHA_API_KEY;
const Train_sitekey = process.env.Sitekey;


const webdriver = require('selenium-webdriver'), // 加入虛擬網頁套件
  By = webdriver.By, // 你想要透過什麼方式來抓取元件，通常使用xpath、css
  until = webdriver.until; // 直到抓到元件才進入下一步(可設定等待時間)
const chrome = require('selenium-webdriver/chrome');
const options = new chrome.Options();
options.addArguments('--log-level=3'); // 這個option可以讓你跟網頁端的console.log說掰掰
// 因為notifications會干擾到爬蟲，所以要先把它關閉
options.setUserPreferences({ 'profile.default_content_setting_values.notifications': 1 });
const axios = require("axios");
const Captcha = require("2captcha");
const Captcha_Solver = new Captcha.Solver(CAPTCHA_Key);

const Solver = async () => {
  console.log("Solving captcha...");
  const { data } = await Captcha_Solver.recaptcha(
    Train_sitekey,
    "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/queryTrain"
  );

  try {
    console.log(data);
  } catch (e) {
    console.log(e);
  }
};

async function ReserveTrainTicket () {
  
  // 建立這個browser的類型
  let driver = await new webdriver.Builder().forBrowser("chrome").withCapabilities(options).build(); // 建立這個Browser的類型
  const web = 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query';//填寫你想要前往的網站 - 台鐵個人訂票
  await driver.get(web); // 透過這個driver打開網頁,在這裡要用await確保打開完網頁後才能繼續動作

   // 填入訂票資訊
   const UserId = await driver.wait(until.elementLocated(By.xpath('//*[@id="pid"]'))); // 找出填寫位置
   UserId.sendKeys(user_Id); // 將使用者的身分證填入

   const StartStation = await driver.wait(until.elementLocated(By.xpath('//*[@id="startStation1"]'))); // 找出填寫位置
   StartStation.sendKeys(user_StartStation); // 將使用者的起程站填入
   const TargetStation = await driver.wait(until.elementLocated(By.xpath('//*[@id="endStation1"]')));// 找出填寫位置
   TargetStation.sendKeys(user_TargetStation);// 將使用者的抵達站填入
   const TrainNumber = await driver.wait(until.elementLocated(By.xpath('//*[@id="trainNoList1"]')));// 找出填寫位置
   TrainNumber.sendKeys(user_TrainNumber);// 將使用者的欲搭乘班次填入
   const RideDate = await driver.wait(until.elementLocated(By.xpath('//*[@id="rideDate1"]')));// 找出填寫位置
   RideDate.clear();// 將預設資訊清除
   RideDate.sendKeys(user_Time);// 將使用者的欲搭乘時間填入
 
   // 抓到查詢按鈕然後點擊
   const Query = await driver.wait(until.elementLocated(By.xpath('//*[@id="queryForm"]/div[5]/input')));
   Query.click();


    //跳轉到下一頁面，拿到結果
    //抓到訂選的班次CheckBox然後點擊
    const Train_Selection = await driver.wait(until.elementLocated(By.xpath('//*[@id="queryForm"]/div[1]/table/tbody/tr[2]/td[10]/label')));
    Train_Selection.click();

    //抓到我不是機器人位置然後點擊 - 目前有問題
    await driver.wait(Solver());

    //抓到下一步按鈕然後點擊
    const NextButton = await driver.wait(until.elementLocated(By.xpath('//*[@id="queryForm"]/div[2]/button[2]')));
    NextButton.click();

}
ReserveTrainTicket(); // 預訂車票