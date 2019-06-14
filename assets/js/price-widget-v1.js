
function renderWidget(widgetElement, wineJson) {
    console.log(wineJson);
    function renderMerchantPrice(price) {
        return `<li class="list-group-item findwine_detail-list">
  <div class="findwine_merchant-holder">
    <div class="findwine_merchant-name"> ${price.merchant}</div>
  </div>
  <div class="findwine_merchant-pricing">
    <div class="findwine_merchant-price-holder">
      <div class="findwine_merchant-currency"> R</div>
      <div class="findwine_vintage-price"> ${price.price}</div>
    </div>
    <a class="btn findwine_buy-button buy-link" href="${wineJson.buy_url}" target="_blank" role="button"> BUY</a>
  </div>
</li>`;
    }
    let priceList = wineJson.price_data.listings.map(renderMerchantPrice);
    let priceHtml = priceList.join('');
    widgetElement.innerHTML = `<ul class="list-group list-group-flush">${priceHtml}</ul>`;
}

document.addEventListener('DOMContentLoaded', function() {
    // todo change in production
    let apiRoot = 'http://localhost:8000/api/wine-prices/';
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

