#! /bin/sh

I18NDOMAIN="collective.newsflash"

# Synchronise the templates and scripts with the .pot.
# All on one line normally:
bin/i18ndude rebuild-pot --pot src/collective/newsflash/locales/${I18NDOMAIN}.pot \
    --create ${I18NDOMAIN} \
   .

# Synchronise the resulting .pot with all .po files
for po in src/collective/newsflash/locales/*/LC_MESSAGES/${I18NDOMAIN}.po; do
    bin/i18ndude sync --pot src/collective/newsflash/locales/${I18NDOMAIN}.pot $po
done