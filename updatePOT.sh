#! /bin/sh
# Linux script for regenerate the Cheese Boys i18n infos

pygettext -d cheeseboys -o cheeseboys.pot -p data/i18n/ *
