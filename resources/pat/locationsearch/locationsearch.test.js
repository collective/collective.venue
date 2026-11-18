import { jest } from "@jest/globals";
import Pattern from "./locationsearch";
import utils from "@patternslib/patternslib/src/core/utils";

const FORM = `
    <form action="http://site/venue/@@edit">
        <input name="form.widgets.IBasic.title" value="Library" />
        <input name="form.widgets.IAddress.street" value="Main street 1" />
        <input name="form.widgets.IAddress.zip_code" value="3100" />
        <input name="form.widgets.IAddress.city" value="St. Pölten" />
        <select name="form.widgets.IAddress.country:list">
            <option value="--NOVALUE--">No value</option>
            <option value="AT" selected>Austria</option>
        </select>
        <div class="geolocation_wrapper edit">
            <input class="latitude" />
            <input class="longitude" />
        </div>
    </form>
`;

const mock_fetch = (geodata) =>
  jest.fn(async (url) => {
    url = new URL(url);
    if (url.pathname.endsWith("plonejsi18n")) {
      return {
        ok: true,
        json: async () => ({ "Search location": "Ort suchen" }),
      };
    }
    return { ok: true, json: async () => geodata };
  });

describe("pat-collective-venue-locationsearch", () => {
  afterEach(() => {
    document.body.innerHTML = "";
    jest.restoreAllMocks();
  });

  it("adds a translated search button and fills in the coordinates", async () => {
    document.documentElement.lang = "de";
    document.body.innerHTML = FORM;
    global.fetch = mock_fetch({ latitude: 48.2, longitude: 15.6 });

    const el = document.querySelector(".geolocation_wrapper");
    new Pattern(el);
    await utils.timeout(1);

    const button = el.querySelector("button.locationsearch");
    expect(button.textContent).toBe("Ort suchen");
    expect(button.type).toBe("button");

    const changed = jest.fn();
    el.querySelector("input.latitude").addEventListener("change", changed);

    await el["pattern-collective-venue-locationsearch"].search();

    const url = new URL(global.fetch.mock.calls.at(-1)[0]);
    expect(url.pathname).toBe("/venue/@@locationsearch");
    expect(Object.fromEntries(url.searchParams)).toEqual({
      title: "Library",
      street: "Main street 1",
      zip_code: "3100",
      city: "St. Pölten",
      country: "Austria",
    });
    expect(el.querySelector("input.latitude").value).toBe("48.2");
    expect(el.querySelector("input.longitude").value).toBe("15.6");
    expect(changed).toHaveBeenCalled();
    expect(button.disabled).toBe(false);
  });

  it("alerts if no location was found", async () => {
    document.body.innerHTML = FORM;
    global.fetch = mock_fetch({ latitude: null, longitude: null });
    const alert = jest.spyOn(window, "alert").mockImplementation(() => {});

    const el = document.querySelector(".geolocation_wrapper");
    new Pattern(el);
    await utils.timeout(1);
    await el["pattern-collective-venue-locationsearch"].search();

    expect(alert).toHaveBeenCalledWith("Could not find an address.");
    expect(el.querySelector("input.latitude").value).toBe("");
  });

  it("does nothing without address fields", async () => {
    document.body.innerHTML = `
            <form><div class="geolocation_wrapper edit"></div></form>
        `;
    global.fetch = mock_fetch({});
    const el = document.querySelector(".geolocation_wrapper");
    new Pattern(el);
    await utils.timeout(1);

    expect(el.querySelector("button")).toBeNull();
    expect(global.fetch).not.toHaveBeenCalled();
  });
});
