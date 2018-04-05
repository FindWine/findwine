import React from 'react';


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
          {this.props.wines.map((winevintage, index) => {
            const imageUrl = winevintage.image_url ? winevintage.image_url : constructImagePath('wine/images/other/placeholder.jpg');
            return (
              <a href={winevintage.details_url} key={index} >
                <div className="findwine_search-results">
                  <div className="findwine_search-result--table">
                    <div className={`findwine_vintage-rating--box findwine_vintage-rating findwine_rating-box-${winevintage.rating_category}`}> {winevintage.rating_display} </div>
                    <div className="findwine_vintage--image">
                      <img src={ imageUrl } alt={winevintage.wine.name } className="img-fluid rounded findwine_vintage--image-img" id="image"/>
                    </div>
                    <div className="findwine_vintage-details">
                      <div className="findwine_vintage-producer">
                        {winevintage.wine.producer}
                      </div>
                      <h4 className="findwine_vintage-vintage" id="wine">
                        {winevintage.wine.name } { winevintage.year }
                      </h4>
                      <div className="findwine_vintage-row">
                        <p className="findwine_vintage-category">
                          { winevintage.sub_category }
                        </p>
                        <div className="findwine_vintage-table--display hidden-sm-up">
                          <div className="findwine_vintage-currency"> R </div>
                          <div className="findwine_vintage-price"> {winevintage.price} </div>
                        </div>
                      </div>
                    </div>
                    <div className="findwine_vintage-table--display findwine_vintage-table--display-search hidden-sm-down">
                      <div className="findwine_vintage-currency"> R </div>
                      <div className="findwine_vintage-price"> {winevintage.price} </div>
                      <button className="btn findwine_view-button"
                              href={winevintage.details_url} target="_self"
                              role="button"> View
                        <img src={ constructImagePath('wine/images/SVGs/arrow-right-white.svg') }
                             className="findwine_view-button-arrow"></img>
                      </button>
                    </div>
                  </div>
                </div>
              </a>
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
