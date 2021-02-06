const puppeteer = require("puppeteer");

const BASE = process.env.BASE;

describe("home page", () => {
  let browser;

  beforeAll(async () => {
    browser = await puppeteer.launch({
      args: ["--no-sandbox", "--disable-setuid-sandbox"],
      executablePath: process.env.CHROME_EXE_PATH || "",
    });
  });

  it("renders full page on desktop", async () => {
    const page = await browser.newPage();
    await page.goto(BASE, {
      waitUntil: "networkidle0",
    });

    await page.waitForTimeout(2000);

    await page.setViewport({
      width: 1280,
      height: 960,
    });

    const image = await page.screenshot();

    expect(image).toMatchImageSnapshot();
  });

  it("renders ipad viewport", async () => {
    const page = await browser.newPage();
    await page.goto(BASE, {
      waitUntil: "networkidle0",
    });
    await page.waitForTimeout(2000); // wait for animation on home page
    await page.setViewport({ width: 1024, height: 768 });
    const image = await page.screenshot();

    expect(image).toMatchImageSnapshot();
  });

  it("renders iphone viewport", async () => {
    const page = await browser.newPage();
    await page.goto(BASE, {
      waitUntil: "networkidle0",
    });
    await page.waitForTimeout(2000); // wait for animation on home page
    await page.setViewport({ width: 372, height: 812 });
    const image = await page.screenshot();

    expect(image).toMatchImageSnapshot();
  });

  afterAll(async () => {
    await browser.close();
  });
});
