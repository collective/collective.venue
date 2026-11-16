define([
    'jquery',
    'pat-base',
    'translate',
    'text!collective-venue-url/locationsearch.xml',
], function($, Base, _t, LocationSearchTemplate) {
    'use strict';

    var LocationSearch = Base.extend({
        name: 'collective-venue-locationsearch',
        trigger: '.geolocation_wrapper.edit',
        parser: 'mockup',

        init: function() {

            var tpl = _.template(LocationSearchTemplate)({_t: _t});
            this.$el.prepend(tpl);

            $('button.locationsearch', this.$el).on('click', function (e) {

                e.preventDefault();

                var form = this.$el.closest('form');

                var title = $('input#form-widgets-IBasic-title', form).val(),
                    street = $('input#form-widgets-IAddress-street', form).val(),
                    zip_code = $('input#form-widgets-IAddress-zip_code', form).val(),
                    city = $('input#form-widgets-IAddress-city', form).val(),
                    country = $('select#form-widgets-IAddress-country option:selected', form).text();

                $.ajax('@@locationsearch', {
                    dataType: 'json',
                    data: {
                        title: title,
                        street: street,
                        zip_code: zip_code,
                        city: city,
                        country: country
                    }
                }).done(function (data) {
                    if (data.latitude && data.longitude) {
                        $('input.latitude', this.$el).val(data.latitude).trigger('change');
                        $('input.longitude', this.$el).val(data.longitude).trigger('change');
                    } else {
                        window.alert(_t('Could not find an address.'))
                    }
                }.bind(this));

            }.bind(this));


        }

    });

    return LocationSearch;

});
