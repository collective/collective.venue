/**
 * Minimal, dependency-free translation helper.
 *
 * Loads the message catalog of a gettext domain from Plone's
 * ``@@plonejsi18n`` view - the same endpoint Mockup's i18n uses, but without
 * jQuery and with a Promise, so that callers can await the catalog before
 * rendering.
 */

const catalogs = new Map();

const current_language = () => {
  const [lang, region] = (document.documentElement.lang || "en").split("-");
  return region ? `${lang}_${region.toUpperCase()}` : lang;
};

const catalog_url = (domain, language) => {
  const base_url = document.body.dataset.i18ncatalogurl || "/plonejsi18n";
  const url = new URL(base_url, window.location.href);
  url.searchParams.set("domain", domain);
  url.searchParams.set("language", language);
  return url;
};

const load_catalog = async (domain, language) => {
  try {
    const response = await fetch(catalog_url(domain, language));
    if (!response.ok) {
      return {};
    }
    return (await response.json()) || {};
  } catch {
    // No translations available - fall back to the msgids.
    return {};
  }
};

/**
 * Return a translation function for a domain.
 *
 * @param {string} domain - The gettext domain.
 * @param {string} [language] - The language. Defaults to the ``lang``
 *     attribute of the ``<html>`` element.
 * @returns {Promise<function(string): string>} - Resolves to a function,
 *     which translates a msgid or returns the msgid itself if no
 *     translation is available.
 */
export const message_factory = async (
  domain,
  language = current_language(),
) => {
  const key = `${domain}-${language}`;
  if (!catalogs.has(key)) {
    catalogs.set(key, load_catalog(domain, language));
  }
  const catalog = await catalogs.get(key);
  return (msgid) => catalog[msgid] || msgid;
};

export default message_factory;
