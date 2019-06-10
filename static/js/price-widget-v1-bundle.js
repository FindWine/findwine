/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 510);
/******/ })
/************************************************************************/
/******/ ({

/***/ 510:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


function renderWidget(widgetElement, wineJson) {
    console.log(wineJson);
    function renderMerchantPrice(price) {
        return '<li class="list-group-item findwine_detail-list">\n  <div class="findwine_merchant-holder">\n    <div class="findwine_merchant-name"> ' + price.merchant + '</div>\n    <div class="findwine_merchant-unit"> 750 ml\n\n        (minimum 6)\n\n    </div>\n    <div class="findwine_merchant-delivery"> Delivery: R50 Cape Town, R75 nation-wide, free for orders of R1000 or more.</div>\n  </div>\n  <div class="findwine_merchant-pricing">\n    <div class="findwine_merchant-price-holder">\n      <div class="findwine_merchant-currency"> R</div>\n      <div class="findwine_vintage-price"> ' + price.price + '</div>\n    </div>\n    <a class="btn findwine_buy-button buy-link" data-merchant="Cybercellar" data-wine-vintage="Flagstone Longitude 2015" href="https://www.cybercellar.com/flagstone-wines-flagstone-longitude-2015?utm_medium=affiliates&amp;utm_source=findwine" target="_blank" role="button"> BUY</a>\n  </div>\n</li>';
    }
    var priceList = wineJson.price_data.listings.map(renderMerchantPrice);
    var priceHtml = priceList.join('');
    widgetElement.innerHTML = '<ul class="list-group list-group-flush">' + priceHtml + '</ul>';
}

document.addEventListener('DOMContentLoaded', function () {
    // todo change in production
    var apiRoot = 'http://localhost:8000/catalog/api/wines/';
    var widget = document.getElementById("findwine-price-widget");
    if (!widget) {
        // todo: improve this message
        console.error("Could not find price div. Did you include the right HTML snippet on the page?");
    } else {
        var wineId = widget.dataset.findwineId;
        var url = '' + apiRoot + wineId + '/';
        console.log(url);
        fetch(url).then(function (response) {
            if (response.ok) {
                response.json().then(function (responseJson) {
                    renderWidget(widget, responseJson);
                });
            }
        });
    }
}, false);

/***/ })

/******/ });