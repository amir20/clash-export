const puppeteer = require("puppeteer");

const BASE = process.env.BASE;

describe("jest-image-snapshot usage with an image received from puppeteer", () => {
  let browser;

  beforeAll(async () => {
    browser = await puppeteer.launch({
      args: ["--no-sandbox", "--disable-setuid-sandbox"],
      executablePath: process.env.CHROME_EXE_PATH || "",
      defaultViewport: { width: 1280, height: 1080 }
    });
  });

  it("captures screenshot", async () => {
    const page = await browser.newPage();
    await page.goto(BASE, {
      waitUntil: "networkidle0"
    });
    await page.waitFor(2000); // wait for animation on home page
    const image = await page.screenshot({ fullPage: true });

    expect(image).toMatchImageSnapshot();
  });

  // xit("captures screenshot reddit dynasty", async () => {
  //   const page = await browser.newPage();
  //   await page.goto("http://localhost:8000/clan/reddit-dynasty-ugjpvjr", {
  //     waitUntil: "networkidle0"
  //   });
  //   const image = await page.screenshot({ fullPage: true });

  //   expect(image).toMatchImageSnapshot({
  //     failureThreshold: "0.05",
  //     failureThresholdType: "percent"
  //   });
  // });

  afterAll(async () => {
    await browser.close();
  });
});
