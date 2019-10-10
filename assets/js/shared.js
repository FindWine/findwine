import React from 'react';
import ReactDOM from 'react-dom';

export class WineRow extends React.Component {
  render() {
      // this separation is necessary because otherwise the whole row is clickable in partner mode
      if (this.props.partnerMode) {
          return this._renderPartnerMode();
      } else {
          return this._render();
      }
  }

  _render() {
      const imageUrl = this.props.wineVintage.image_url ? this.props.wineVintage.image_url : constructImagePath('wine/images/other/placeholder.jpg');
      return (
          <a href={this.props.wineVintage.details_url} target="_blank">
            <div className="findwine_search-results">
                {this._renderWine()}
            </div>
          </a>
      );
  }

  _renderPartnerMode() {
      return (
          <div>
              <div className="findwine_search-results">
                {this._renderWine()}
            </div>
          </div>
      );
  }

  _getDisplayClassPartnerHidden() {
      return this.props.partnerMode ? 'd-none' : '';
  }

  _getDisplayClassPartnerVisible() {
      return this.props.partnerMode ? '': 'd-none';
  }

  _renderWine() {
      const imageUrl = this.props.wineVintage.image_url ? this.props.wineVintage.image_url : constructImagePath('wine/images/other/placeholder.jpg');
      return (
          <div className="findwine_search-result--table">
            <div className={`${this._getDisplayClassPartnerHidden()} findwine_vintage-rating--box findwine_vintage-rating findwine_rating-box-${this.props.wineVintage.rating_category}`}> {this.props.wineVintage.rating_display} </div>
            <div className={`findwine_vintage--image ${this.props.partnerMode ? 'partner-mode' : ''}`}>
              <img src={ imageUrl } alt={this.props.wineVintage.wine.name } className="img-fluid rounded findwine_vintage--image-img" id="image"/>
            </div>
            <div className="findwine_vintage-details">
              <div className="findwine_vintage-producer">
                {this.props.wineVintage.wine.producer}
              </div>
              <h4 className="findwine_vintage-vintage" id="wine">
                {this.props.wineVintage.wine.name } { this.props.wineVintage.year }
              </h4>
              <div className={`findwine_vintage-row ${this._getDisplayClassPartnerHidden()}`}>
                <p className="findwine_vintage-category">
                  { this.props.wineVintage.sub_category }
                </p>
                <div className="findwine_vintage-table--display hidden-sm-up">
                    {this._getPriceElement(this.props.wineVintage)}
                </div>
              </div>
            </div>
            <div className={`findwine_vintage-table--display findwine_vintage-table--display-search hidden-sm-down ${this._getDisplayClassPartnerHidden()}`}>
              {this._getPriceElement(this.props.wineVintage)}
              <a href={this.props.wineVintage.details_url} target="_blank">
                  <button className="btn findwine_view-button"
                          href={this.props.wineVintage.details_url} target="_blank"
                          role="button"> View
                    <img src={ constructImagePath('wine/images/SVGs/arrow-right-white.svg') }
                         className="findwine_view-button-arrow"></img>
                  </button>
              </a>
            </div>
            <div className={`embed-info ${this._getDisplayClassPartnerVisible()}`}>
                <strong>Embed code (popup)</strong>
                <pre><code>
                    &lt;div class=&quot;findwine-price-widget&quot; data-findwine-id=&quot;{this.props.wineVintage.slug}&quot; data-findwine-is-modal &gt;&lt;/div&gt;
                </code></pre>
            </div>
            <div className={`embed-info ${this._getDisplayClassPartnerVisible()}`}>
                <strong>Embed code (direct)</strong>
                <pre><code>
                    &lt;div class=&quot;findwine-price-widget&quot; data-findwine-id=&quot;{this.props.wineVintage.slug}&quot; &gt;&lt;/div&gt;
                </code></pre>
            </div>
          </div>
      );
  }
  _getPriceElement(winevintage) {
    var currencyDisplay = winevintage.available ? 'R' : 'Unavailable';
    var priceDisplay = winevintage.available ? winevintage.price : '';
    return (
      <div>
        <div className="findwine_vintage-currency"> {currencyDisplay} </div>
        <div className="findwine_vintage-price"> {priceDisplay} </div>
      </div>
    );
  };

}


export class WineList extends React.Component {
  render() {
    if (this.props.isLoading) {
      return (
        <div className="text-center">
          <img src={ constructImagePath('wine/images/other/loading.gif')} alt="loading..." />
          <p>Loading wines...</p>
        </div>
      );
    }
    else if (this.props.wines.length > 0) {
      return (
        <div className="findwine_vintage-table">
          {this._renderPartnerInfo()}
          {this.props.wines.map((winevintage, index) => {
            return (
                <WineRow wineVintage={winevintage} partnerMode={this.props.partnerMode} key={index} />
            );
          })}
        </div>
      );
    } else {
      return (
        <div className="findwine_no-results-holder">
          <img src={ constructImagePath('wine/images/SVGs/no-results.svg') } className="findwine_no-results-holder-image"></img>
          <p className="findwine_no-results-text-heading"> No results found. </p>
          <p className="findwine_no-results-text"> Please adjust your search criteria. </p>
        </div>
      );
    }
  }

  _renderPartnerInfo() {
      if (this.props.partnerMode) {
          return <p>For more details on how to use embed codes see <a href="/partners/" target="_blank">this page</a>.</p>
      } else {
          return '';
      }
  }
}

export class Paginator extends React.Component {
  render() {
    // let nextButton = this.props.showNext ? `<a onClick=${(event) => this.props.nextPage()}>Next</a>` : '';
    let nextButton = this.props.showNext ?
      <a className="btn findwine_search-next--button" href="#top" onClick={(event) => this.props.nextPage()}>
        <p className="findwine_search-next--button-text hidden-sm-down">Next</p>
        <img src={constructImagePath('wine/images/SVGs/arrow-right.svg')} alt="Next" className="findwine_search-next--button-arrow-right"></img>
      </a> : <a className="btn findwine_search-next--button-inactive" onClick={(event) => this.props.nextPage()}>
      <p className="findwine_search-next--button-text-inactive hidden-sm-down">Next</p>
      <img src={constructImagePath('wine/images/SVGs/arrow-right-greyLight.svg')} alt="Next" className="hidden-md-up"></img>
      <img src={constructImagePath('wine/images/SVGs/arrow-left-green.svg')} alt="Next" className="hidden-sm-down findwine_search-next--button-green-arrow-right"></img>
    </a>;
    let prevButton = this.props.showPrevious ?
      <a className="btn findwine_search-next--button findwine_search-next--button-left" href="#top" onClick={(event) => this.props.prevPage()}>
        <img src={constructImagePath('wine/images/SVGs/arrow-right.svg')} alt="Previous" className="findwine_search-next--button-arrow"></img>
        <p className="findwine_search-next--button-text hidden-sm-down">Previous</p>
      </a> : <a className="btn findwine_search-next--button-inactive findwine_search-next--button-left" onClick={(event) => this.props.nextPage()}>
      <img src={constructImagePath('wine/images/SVGs/arrow-left-grey.svg')} alt="Previous" className="hidden-md-up"></img>
      <img src={constructImagePath('wine/images/SVGs/arrow-left-green.svg')} alt="Previous" className="hidden-sm-down findwine_search-next--button-green-arrow"></img>
      <p className="findwine_search-next--button-text-inactive hidden-sm-down">Previous</p>
    </a>;

      return (
      <div className="findwine_search-page--container">
        <div className="findwine_search-page--inner">
          <div className="findwine_search-page"> Page {this.props.page} </div>
          <div className="findwine_search-winesTotal"> {this.props.start} - {this.props.end} of {this.props.count} wines </div>
        </div>
        <div className="findwine_search-button--container">
          {prevButton}
          {nextButton}
        </div>
      </div>
    )
  }
}

export function constructImagePath(path) {
  // assumes defined on the page.
  return `${STATIC_BASE_PATH}${path}`;
}
