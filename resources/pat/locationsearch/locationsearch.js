/**
 * collective-venue-locationsearch
 *
 * Adds a "Search location" button to the geolocation edit widget of
 * plone.formwidget.geolocation. On click, the address entered in the form is
 * geocoded via the ``@@locationsearch`` view and the resulting coordinates
 * are written into the latitude and longitude fields.
 */
import { BasePattern } from "@patternslib/patternslib/src/core/basepattern";
import registry from "@patternslib/patternslib/src/core/registry";
import message_factory from "../../i18n";

const DOMAIN = "collective.venue";

// Form fields, which are used to build the address query.
// The first matching selector wins. Multiple selectors per field allow for
// different behaviors providing the title.
const FIELDS = {
  title: [
    "[name='form.widgets.IBasic.title']",
    "[name='form.widgets.IDublinCore.title']",
    "[name='form.widgets.title']",
  ],
  street: ["[name='form.widgets.IAddress.street']"],
  zip_code: ["[name='form.widgets.IAddress.zip_code']"],
  city: ["[name='form.widgets.IAddress.city']"],
  country: ["select[name^='form.widgets.IAddress.country']"],
};

const field_value = (form, selectors) => {
  for (const selector of selectors) {
    const field = form.querySelector(selector);
    if (!field) {
      continue;
    }
    if (field.tagName === "SELECT") {
      // The geocoder needs the country name, not the country code.
      const option = field.selectedOptions[0];
      return option && option.value !== "--NOVALUE--"
        ? option.textContent.trim()
        : "";
    }
    return field.value.trim();
  }
  return "";
};

const set_value = (input, value) => {
  if (!input) {
    return;
  }
  input.value = value;
  // Notify listeners, e.g. pat-leaflet to update the marker.
  input.dispatchEvent(new Event("input", { bubbles: true }));
  input.dispatchEvent(new Event("change", { bubbles: true }));
};

class Pattern extends BasePattern {
  static name = "collective-venue-locationsearch";
  static trigger = ".geolocation_wrapper.edit";

  async init() {
    this.form = this.el.closest("form");
    if (!this.form) {
      return;
    }

    const has_address = ["street", "zip_code", "city"].some((name) =>
      this.form.querySelector(FIELDS[name][0]),
    );
    if (!has_address) {
      // Nothing to search for.
      return;
    }

    this._t = await message_factory(DOMAIN);

    this.button = document.createElement("button");
    this.button.type = "button";
    this.button.classList.add("locationsearch", "btn", "btn-primary");
    this.button.textContent = this._t("Search location");
    this.button.addEventListener("click", () => this.search());
    this.el.prepend(this.button);
  }

  async search() {
    const query = {};
    for (const [name, selectors] of Object.entries(FIELDS)) {
      query[name] = field_value(this.form, selectors);
    }

    const url = new URL(
      "@@locationsearch",
      this.form.action || window.location.href,
    );
    url.search = new URLSearchParams(query).toString();

    this.button.disabled = true;
    this.button.setAttribute("aria-busy", "true");
    let data = {};
    try {
      const response = await fetch(url, {
        headers: { Accept: "application/json" },
      });
      if (response.ok) {
        data = await response.json();
      }
    } catch {
      // Handled below like an empty result.
    } finally {
      this.button.disabled = false;
      this.button.removeAttribute("aria-busy");
    }

    if (data.latitude && data.longitude) {
      set_value(this.el.querySelector("input.latitude"), data.latitude);
      set_value(this.el.querySelector("input.longitude"), data.longitude);
    } else {
      window.alert(this._t("Could not find an address."));
    }
  }
}

registry.register(Pattern);

export default Pattern;
export { Pattern };
