(function($) {
    $(document).ready(function() {
        const tourSelect = $('#id_tour');
        const agePricesField = $('#id_age_prices');
        const extraPricesField = $('#id_extra_prices');

        agePricesField.prop('disabled', true);
        extraPricesField.prop('disabled', true);

        tourSelect.change(function() {
            const tourId = $(this).val();

            if (!tourId) {
                agePricesField.empty().prop('disabled', true);
                extraPricesField.empty().prop('disabled', true);
                return;
            }

            $.ajax({
                url: '/admin/get-related-prices/',  // ✅ This must match your urlpatterns
                data: { tour_id: tourId },
                success: function(data) {
                    agePricesField.empty();
                    extraPricesField.empty();

                    data.age_prices.forEach(function(item) {
                        agePricesField.append(
                            $('<option></option>').val(item.id).text(item.name)
                        );
                    });

                    data.extra_prices.forEach(function(item) {
                        extraPricesField.append(
                            $('<option></option>').val(item.id).text(item.name)
                        );
                    });

                    agePricesField.prop('disabled', false);
                    extraPricesField.prop('disabled', false);
                }
            });
        });
    });
})(django.jQuery);
