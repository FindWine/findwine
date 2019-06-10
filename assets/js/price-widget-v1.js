
function renderWidget(widgetElement, wineJson) {
    console.log(wineJson);
    function renderMerchantPrice(price) {
        return `<li class="list-group-item findwine_detail-list">
  <div class="findwine_merchant-holder">
    <div class="findwine_merchant-name"> ${price.merchant}</div>
    <div class="findwine_merchant-unit"> 750 ml

        (minimum 6)

    </div>
    <div class="findwine_merchant-delivery"> Delivery: R50 Cape Town, R75 nation-wide, free for orders of R1000 or more.</div>
  </div>
  <div class="findwine_merchant-pricing">
    <div class="findwine_merchant-price-holder">
      <div class="findwine_merchant-currency"> R</div>
      <div class="findwine_vintage-price"> ${price.price}</div>
    </div>
    <a class="btn findwine_buy-button buy-link" data-merchant="Cybercellar" data-wine-vintage="Flagstone Longitude 2015" href="https://www.cybercellar.com/flagstone-wines-flagstone-longitude-2015?utm_medium=affiliates&amp;utm_source=findwine" target="_blank" role="button"> BUY</a>
  </div>
</li>`;
    }
    let priceList = wineJson.price_data.listings.map(renderMerchantPrice);
    let priceHtml = priceList.join('');
    widgetElement.innerHTML = `<ul class="list-group list-group-flush">${priceHtml}</ul>`;
}

document.addEventListener('DOMContentLoaded', function() {
    // todo change in production
    let apiRoot = 'http://localhost:8000/catalog/api/wines/';
    let widget = document.getElementById("findwine-price-widget");
    if (!widget) {
        // todo: improve this message
        console.error("Could not find price div. Did you include the right HTML snippet on the page?")
    } else {
        let wineId = widget.dataset.findwineId;
        let url = `${apiRoot}${wineId}/`;
        console.log(url);
        fetch(url).then((response) => {
            if (response.ok) {
                response.json().then((responseJson) => {
                    renderWidget(widget, responseJson);
                });
            }
        });


    }


}, false);

