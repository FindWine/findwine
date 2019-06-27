
window.FindWine = (function() {
    function addStyles() {
        let widgetCss = `li.findwine-buy-item {
            display: flex;
            min-width: 200px;
            max-width: 400px;
            justify-content: space-between;
            align-items: center;
            margin: 1rem;
        }
        .findwine-merchant-name {
            font-size: 1.5rem;
        }
        .findwine-merchant-price-currency {
            font-size: 1rem;
            color: grey;
        }
        .findwine-merchant-price-value {
            font-size: 1.5rem;
            font-weight: bold;
        }
        a.findwine-buy-button {
            font-size: 1.5rem;
            margin-left: .5rem;
        }
        a.findwine-buy-button:hover {
            // text-decoration: underline;
        }
        .findwine-no-data {
            font-size: 1rem;
        }
        `;
        // append style to page
        // https://stackoverflow.com/a/524721/8207
        let style = document.createElement('style');
        document.head.appendChild(style);
        style.appendChild(document.createTextNode(widgetCss));

    }

    function renderWidget(widgetElement, partnerId, wineJson) {
        // console.log(wineJson);
        if (wineJson.price_data.listings.length === 0) {
            widgetElement.innerHTML = "<div class='findwine-no-data'>Out of Stock</div>";
        }
        else {
            function renderMerchantPrice(price) {
                return `<li class="findwine-buy-item">
          <div class="findwine-merchant-name"> ${price.merchant.name}</div>
          <div class="findwine-merchant-price">
             <span class="findwine-merchant-price-currency"> R</span>
             <span class="findwine-merchant-price-value"> ${price.price}</span>
             <a class="findwine-buy-button" href="${wineJson.buy_url}?from=${partnerId}&merchant_wine=${price.id}" target="_blank" role="button"> Buy</a>
          </div>
        </li>`;
            }
            let priceList = wineJson.price_data.listings.map(renderMerchantPrice);
            let priceHtml = priceList.join('');

            widgetElement.innerHTML = `<ul class="findwine-buy-list">${priceHtml}</ul>`;
        }
    }

    function init(partnerId) {
        addStyles();
        // swap these for development
        // let apiRoot = 'http://localhost:8000/api/wine-prices/';
        let apiRoot = 'https://www.findwine.com/api/wine-prices/';
        let widgets = document.getElementsByClassName("findwine-price-widget");
        if (!widgets.length) {
            // todo: improve this message
            console.error("Could not find price div. Did you include the right HTML snippet on the page?")
        } else {
            for (let i = 0; i < widgets.length; i++) {
                let widget = widgets[i];
                let wineId = widget.dataset.findwineId;
                let url = `${apiRoot}${wineId}/`;
                fetch(url).then((response) => {
                    if (response.ok) {
                        response.json().then((responseJson) => {
                            renderWidget(widget, partnerId, responseJson);
                        });
                    }
                });
            }
        }
    }

    return {
        init: init
    }
})();
