
window.FindWine = (function() {
    function addStyles() {
        let widgetCss = `
        ul.findwine-buy-list {
            padding-left: 0;
        } 
        li.findwine-buy-item {
            display: flex;
            min-width: 200px;
            max-width: 400px;
            justify-content: space-between;
            align-items: top;
            margin: 1em 0;
        }
        .findwine-merchant-details {
            line-height: 1.1;
        }
        .findwine-merchant-name {
            font-size: 1em;
        }
        .findwine-merchant-extras {
            font-size: .75em;
            color: grey;
        }
        .findwine-merchant-price-currency {
            font-size: .75em;
            color: grey;
        }
        .findwine-merchant-price-value {
            font-size: 1em;
            font-weight: bold;
        }
        a.findwine-buy-button {
            font-size: 1em;
            margin-left: .5em;
        }
        a.findwine-buy-button:hover {
            // text-decoration: underline;
            cursor: pointer;
        }
        li.findwine-no-data {
            font-size: 1em;
        }
        
        .findwine-modal {
            /* https://www.w3schools.com/howto/howto_css_modals.asp */
            display: none;
            position: fixed; /* Stay in place */
            z-index: 10000; /* Sit on top */
            left: 0;
            top: 0;
            width: 100%; /* Full width */
            height: 100%; /* Full height */
            overflow: auto; /* Enable scroll if needed */
            background-color: rgb(0,0,0); /* Fallback color */
            background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
        }
        
        .findwine-modal.is-open {
            display: block;
        }
        
        .findwine-modal-content {
            background-color: #fefefe;
            margin: 15% auto; /* 15% from the top and centered */
            padding: 20px;
            border: 1px solid #888;
            min-width: 300px; /* Could be more or less, depending on screen size */
            max-width: 500px; /* Could be more or less, depending on screen size */
        }
        .findwine-modal-close {
          color: #aaa;
          position: relative;
          font-size: 2em;
          font-weight: bold;
          line-height: 1;
        }
        
        .findwine-modal-close:hover,
        .findwine-modal-close:focus {
          color: black;
          text-decoration: none;
          cursor: pointer;
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
        let priceHtml;
        if (wineJson.price_data.listings.length === 0) {
            priceHtml = "<li class='findwine-buy-item findwine-no-data'>Out of Stock</li>";
        }
        else {
            function renderMerchantPrice(price) {
                return `<li class="findwine-buy-item">
          <div class="findwine-merchant-details">
             <div class="findwine-merchant-name"> ${price.merchant.name}</div>
             <div class="findwine-merchant-extras">
                 <span class="findwine-merchant-unit"> ${price.purchase_unit} ml</span>
                 ${ price.minimum_purchase_unit > 1 ? `<span class="findwine-merchant-minimum">(minimum ${price.minimum_purchase_unit})</span>` : '' }
             </div>
          </div>
          <div class="findwine-merchant-price">
             <span class="findwine-merchant-price-currency"> R</span>
             <span class="findwine-merchant-price-value"> ${price.price}</span>
             <a class="findwine-buy-button" href="${wineJson.buy_url}?from=${partnerId}&merchant_wine=${price.id}" target="_blank" role="button"> Buy</a>
          </div>          
        </li>`;
            }
            let priceList = wineJson.price_data.listings.map(renderMerchantPrice);
            priceHtml = priceList.join('');
        }
        widgetElement.innerHTML = `<ul class="findwine-buy-list">${priceHtml}</ul>`;
    }

    function renderModal(widgetElement, partnerId, wineJson) {
        let modalElt = document.createElement('div');
        modalElt.classList.add('findwine-modal');
        let modalInner = document.createElement('div');
        modalInner.classList.add('findwine-modal-content');
        modalElt.appendChild(modalInner);
        let closeButton = document.createElement('span');
        closeButton.classList.add('findwine-modal-close');
        closeButton.innerHTML = '&times;';
        closeButton.addEventListener('click', function () {
            modalElt.classList.remove('is-open');
        });
        modalInner.appendChild(closeButton);
        let prices = document.createElement('div');
        renderWidget(prices, partnerId, wineJson);
        modalInner.appendChild(prices);
        document.body.appendChild(modalElt);
        if (wineJson.price_data.listings.length === 0) {
            widgetElement.innerHTML = "<li class='findwine-buy-item findwine-no-data'>Out of Stock</li>";
        } else {
            widgetElement.innerHTML = `<button class="findwine-modal-opener">Buy from R${wineJson.price_data.lowest_price}</button>`;
            widgetElement.addEventListener('click', function () {
                modalElt.classList.add('is-open');
            });
        }
    }

    function init(partnerId) {
        /*
        Use inline=true to render the prices directly inline with the widget.
         */
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
                // https://stackoverflow.com/a/18007234/8207
                let isModal = widget.dataset.findwineIsModal !== undefined;
                console.log("is modal", isModal);
                let url = `${apiRoot}${wineId}/`;
                fetch(url).then((response) => {
                    if (response.ok) {
                        response.json().then((responseJson) => {
                            if (isModal) {
                                renderModal(widget, partnerId, responseJson);
                            } else {
                                renderWidget(widget, partnerId, responseJson);
                            }
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
