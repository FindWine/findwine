import "babel-polyfill";
import React from 'react';
import ReactDOM from 'react-dom';
import 'whatwg-fetch';
import Select from 'react-select';
require('rc-slider/assets/index.css');
import Slider, {Range} from 'rc-slider';
const queryString = require('query-string');


// todo: figure out how to django-ize these
const WINE_API_URL = '/api/wine-vintages/';

class CategorySelect extends React.Component {
  render() {
    let choices = getCategoryChoices(this.props.category).map((category) => {
      return {'value': category, 'label': category}
    });

    return (
      <Select
        value={this.props.selectedCategory}
        options={choices}
        onChange={(event) => this.props.categoryChanged(event)}
        multi={false}
        simpleValue={true}
        placeholder='Show all'
      />
    )
  }

}

class CategorySelectMobile extends React.Component {

  render() {
    return (
      <div className="hidden-md-up findwine_button-outer" value={this.props.selectedCategory}>
        {getCategoryChoices().map((category, index) => {
          const isSelected = category === this.props.selectedCategory;
          const classes = `btn btn-secondary findwine_button-category ${isSelected ? 'selected': ''}`;
          const selectedBarClass = `findwine_button-bar--selected${getCategoryId(category)}`;
          const barClasses = `findwine_button-bar ${isSelected ? selectedBarClass : ''}`;
          const image = isSelected ? getSelectedImagePath(category) : getImagePath(category);
          return (
          <button key={index} type="button" className={classes} name={category}
                  onClick={() => this.props.categoryChanged(category)}>
            <div className="findwine_svg">
              <img className="findwine_button-default" src={image}></img>
            </div>
            <div className="findwine_button-type">
                <p value={category}>{category}</p>
            </div>
            <div className={barClasses}>
            </div>
          </button>
        )
        })}
      </div>
    );
  }
}

class SubCategorySelect extends React.Component {
    render() {
        let choices = getSubcategories(this.props.selectedCategory).map((choice) => {
            return {'value': choice, 'label': choice}
        });

        return (
            <Select
                value={this.props.selectedSubcategory}
                options={choices}
                onChange={(event) => this.props.subcategoryChanged(event)}
                multi={true}
                simpleValue={true}
                placeholder='Show all'
            />
        )
    }
}

class SortSelect extends React.Component {

    render() {
        return (
            <select className="form-control" id="id_sort"
                    value={this.props.selectedSort}
                    onChange={(event) => this.props.sortChanged(event.target.value)}>
                {getSortChoices().map((sortChoice, index) => {
                    return (
                        <option key={index} value={sortChoice[1]}>{sortChoice[0]}</option>
                    )
                })}
            </select>
        );
    }
}


class SearchControls extends React.Component {
    constructor() {
        super();
        this.state = {
            isExpanded: false
        }
    }

    _getSortSelect() {
        if (this.props.firstSearchMade) {
            return (
                <div className="col-sm-2">
                    <div className="form-group">
                        <label htmlFor="id_sort">Sort By</label>
                        <SortSelect
                            selectedSort={this.props.selectedSort}
                            sortChanged={this.props.sortChanged}
                        />
                    </div>
                </div>
            );
        }
    }

    _getSearchButton() {
        if (!this.props.firstSearchMade) {
            return (
                <div className="col-lg-12 findwine_button-outer">
                    <button type="submit" className="btn btn-primary btn-block findwine_button"
                            onClick={(event) => this.props.searchClicked(event)}> SEARCH WINES <img src={constructImagePath('wine/images/SVGs/arrow.svg')} alt="search" className="hidden-md-up"></img>
                    </button>
                </div>
            );
        }
    }

    getSlider() {
        const minPriceInt = parseInt(this.props.minPrice) || 0;
        const maxPriceInt = parseInt(this.props.maxPrice) || 500;
        return (
            <Range
                defaultValue={[0,500]}
                max={500}
                value={[minPriceInt, maxPriceInt]}
                allowCross={false}
                onChange={(value) => {
                  this.props.minPriceChanged(value[0], false);
                  this.props.maxPriceChanged(value[1], false);
                }}
                onAfterChange={(value) => {
                  this.props.minPriceChanged(value[0], true);
                  this.props.maxPriceChanged(value[1], true);
                }}
            />
        );
    }

    renderCollapseButton() {
        if (this.props.firstSearchMade && this.state.isExpanded) {
          return (
            <button className="findwine_filters-expand-button" type="button" onClick={() => this.setState({'isExpanded': false})}>
              &#10006;
            </button>
          )
        }
    }

    renderControls() {
        return (
                <form className="search-form" role="search">
                    {this.renderCollapseButton()}
                    <div className="row d-flex align-items-start findwine_search-form">

                        <div className="col-md-3">
                            <div className="form-group category">
                                <label htmlFor="id_category" className="findwine_heading-3">Select wine</label>
                                  <CategorySelectMobile
                                    selectedCategory={this.props.selectedCategory}
                                    categoryChanged={this.props.categoryChanged}
                                  />
                                <div className="hidden-sm-down">
                                    <CategorySelect
                                        selectedCategory={this.props.selectedCategory}
                                        categoryChanged={this.props.categoryChanged}
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="col-md-3">
                            <div className="form-group sub_category">
                                <label htmlFor="id_sub_category" className="findwine_heading-3"> Select type(s)</label>
                                <SubCategorySelect
                                    selectedCategory={this.props.selectedCategory}
                                    selectedSubcategory={this.props.selectedSubcategory}
                                    subcategoryChanged={this.props.subcategoryChanged}
                                />
                            </div>
                        </div>

                        <div className="col-xs-12 col-md-6 findwine_subcategory-row">
                            <div className="col-xs-12 col-md-4 findwine_subcategory" >
                                <div className="form-group sub_category">
                                    <label htmlFor="id_sub_category" className="findwine_heading-3"> Price range </label>
                                </div>
                            </div>
                            {/*Slider - mobile layout slider appears above max and min price*/}
                            <div className="col-xs-12 hidden-md-up">
                                {this.getSlider()}
                            </div>
                            <div className="col-xs-6 col-md-8 findwine_price-input">
                               <div className="form-group min_price">
                                   R <input className="form-control" type="number" name="min_price"
                                          value={this.props.minPrice} min="0" required id="id_min_price"
                                          onChange={(event) => this.props.minPriceChanged(event.target.value, true)}
                                   />
                               </div>
                               <div className="price-range hidden-md-up"> TO </div>
                              <div className="price-range hidden-sm-down"> - </div>
                               <div className="form-group max_price">
                                 R  <input className="form-control" type="number" name="max_price"
                                           value={this.props.maxPrice} min="0" required id="id_max_price"
                                           onChange={(event) => this.props.maxPriceChanged(event.target.value, true)}
                               />
                               </div>
                            </div>
                            <div className="col-md-12 hidden-sm-down">
                               {this.getSlider()}
                            </div>
                        </div>
                        {this._getSortSelect()}
                    </div>
                    {this._getSearchButton()}
                </form>
            );
    }

    renderCollapsedControls() {
        return (
          <div className="findwine_filters-collapsed">
            <div className="findwine_filters-icon">
              <img src={ constructImagePath('wine/images/SVGs/filter.svg')} className="findwine_filters-filter-icon" />
            </div>
            <div className="findwine_filters-filters">
              <div className="findwine_filters-list">
                <div className="findwine_filters-1">
                    { this.props.selectedCategory }
                </div>
                <div className="findwine_filters-bullet"></div>
                <div className="findwine_filters-2">
                    { this.props.selectedSubcategory }
                </div>
                <div className="findwine_filters-bullet"></div>
                <div className="findwine_filters-more">
                  R { this.props.minPrice } - R { this.props.maxPrice }
                </div>
              </div>
            </div>
            <div className="findwine_filters-expand">
              <button className="findwine_filters-expand-button" type="button" onClick={() => this.setState({'isExpanded': true})} style={{outline: 'none', border:'none', background: "none"}}>
                <img src={ constructImagePath('wine/images/SVGs/arrow-down.svg') } className="findwine_filters-expand-arrow" />
              </button>
            </div>
          </div>
        );
    }

    showSearchControls() {
        return !this.props.firstSearchMade || this.state.isExpanded;
    }

    render() {
        if (this.showSearchControls()) {
          return this.renderControls();
        } else {
          return this.renderCollapsedControls();
        }

    }
}

class RatingsExplanationBar extends React.Component {
    render () {
      return (
        <div className="findwine_ratings-explained--container" id="modal">
          <div className="findwine_ratings-heading">
              Ratings explained
          </div>
          <button type="button" className="findwine_ratings-info" data-toggle="modal" data-target="#ratingsExplained" style={{outline: 'none', border:'none', background: "none"}}>
            <img src={ constructImagePath('wine/images/SVGs/info.svg') } className="findwine_ratings-info-icon" />
          </button>
        </div>
      );
    }
}

class RatingsModal extends React.Component {
  render() {
    return (
      <div class="modal fade" id="ratingsExplained" tabindex="-1" role="dialog" aria-labelledby="ratingsExplainedLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-body findwine_modal">
              <div class="findwine_modal-ratings">
                <img src={ constructImagePath('wine/images/SVGs/ratings.svg') } class="findwine_modal-ratings-icon" />
              </div>
              <div class="findwine_modal-heading">
                Ratings Explained
              </div>
              <div class="findwine_modal-content">
                Maecenas vitae ligula quis nunc pharetra rhoncus. Nunc in lacus vitae tortor gravida consequat quis id tortor.
                In ullamcorper ligula justo, at varius purus vulputate vel. Suspendisse vel pharetra risus, eu vulputate nulla.
                Sed at congue nisl, et pellentesque nisi. Maecenas vitae ligula quis nunc pharetra.
              </div>
            </div>
            <div class="modal-footer findwine_modal-footer">
              <button type="button" class="btn btn-secondary findwine_modal-button" data-dismiss="modal">Got it</button>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

class WineList extends React.Component {
    render() {
        if (this.props.wines.length > 0) {
            return (

                <table className="table table-responsive table-sm findwine_vintage-table">
                    <tbody>
                    {this.props.wines.map((winevintage, index) => {
                        return (
                            <tr key={index} className="findwine_search-results">
                                <td className="findwine_search-result--table">
                                  <div className={`findwine_vintage-rating--box findwine_vintage-rating findwine_rating-box-${winevintage.rating_category}`}> {winevintage.avg_rating} </div>
                                  <div className="findwine_vintage--image">
                                    <img src={ winevintage.image_url } alt={winevintage.wine.name } className="img-fluid rounded findwine_vintage--image-img"/>
                                  </div>
                                  <div className="findwine_vintage-details">
                                    <a className="findwine_vintage-producer" href={winevintage.details_url}>
                                      {winevintage.wine.producer}
                                    </a>
                                    <h4 className="findwine_vintage-vintage"> {winevintage.wine.name } { winevintage.year } </h4>
                                    <p className="findwine_vintage-category">
                                      { winevintage.sub_category }
                                    </p>
                                  </div>
                                </td>
                                <td className="findwine_vintage-table--display">
                                  <div className="findwine_vintage-currency"> R </div>
                                  <div className="findwine_vintage-price"> {winevintage.price} </div>
                                  <a class="btn findwine_buy-button hidden-sm-down" href={winevintage.details_url} target="_blank" role="button"> View
                                    <img src={ constructImagePath('wine/images/SVGs/arrow-right-white.svg') } class="findwine_detail-right-arrow"></img>
                                  </a>
                                </td>
                            </tr>
                        );
                    })}
                    </tbody>
                </table>
            );
        } else {
            return (
              <div className="findwine_no-results-holder">
                <img src={ constructImagePath('wine/images/SVGs/no-results.svg') } class="findwine_no-results-holder-image"></img>
                <p className="findwine_no-results-text-heading"> No results found. </p>
                <p className="findwine_no-results-text"> Please adjust your serch criteria. </p>
              </div>
            )
        }
    }
}

/**
 *  <div className="findwine_merchant-currency"> R </div> <div className="findwine_merchant-price"> {{ merchantwine.price }} </div>
 */

class Paginator extends React.Component {
    render() {
        // let nextButton = this.props.showNext ? `<a onClick=${(event) => this.props.nextPage()}>Next</a>` : '';
        let nextButton = this.props.showNext ?
            <a className="btn findwine_search-next--button" href="#modal" onClick={(event) => this.props.nextPage()}>
              <p className="findwine_search-next--button-text hidden-sm-down">Next</p>
              <img src={constructImagePath('wine/images/SVGs/arrow-right.svg')} alt="Next" className="findwine_search-next--button-arrow-right"></img>
            </a> : <a className="btn findwine_search-next--button-inactive" onClick={(event) => this.props.nextPage()}>
            <p className="findwine_search-next--button-text-inactive hidden-sm-down">Next</p>
            <img src={constructImagePath('wine/images/SVGs/arrow-right-greyLight.svg')} alt="Next" className="hidden-md-up"></img>
            <img src={constructImagePath('wine/images/SVGs/arrow-left-green.svg')} alt="Next" className="hidden-sm-down findwine_search-next--button-green-arrow-right"></img>
          </a>;
        let prevButton = this.props.showPrevious ?
            <a className="btn findwine_search-next--button findwine_search-next--button-left" href="#modal" onClick={(event) => this.props.prevPage()}>
              <img src={constructImagePath('wine/images/SVGs/arrow-left.svg')} alt="Previous" className="findwine_search-next--button-arrow"></img>
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
                <div className="findwine_search-winesTotal"> {this.props.start}-{this.props.end} of {this.props.count} wines </div>
              </div>
              <div className="findwine_search-button--container">
                {prevButton}
                {nextButton}
              </div>
            </div>
        )
    }
}

class SearchPage extends React.Component {
    constructor() {
        super();
        // initialize with first category / subcategory selected
        const category = getCategoryChoices()[0];
        this.state = {
            selectedCategory: null,
            selectedSubcategory: null,
            minPrice: 0,
            maxPrice: 500,
            selectedSort: getSortChoices()[0][1],
            // results / pagination
            wines: [],
            resultCount: 0,
            resultPage: 1,
            resultStart: 1,
            resultEnd: 10,
            nextPageUrl: null,
            prevPageUrl: null,
            firstSearchMade: false,
        }
    }

    componentDidMount() {
        let queryParams = queryString.parse(location.search);
        if (Object.keys(queryParams).length) {
            queryParams['firstSearchMade'] = true;
            this._updateLandingPage(true);
            this.setState(queryParams, this._updateSearchResults);
        }
        // there might be a better way to do this
        // clear search results on back button press back to home page
        var self = this;
        let showLandingPageContent = () => this._updateLandingPage(false);
        $(window).on('popstate', function (e) {
            if (location.pathname === '/') {
                self.setState(
                  {
                    'firstSearchMade': false
                  },
                  showLandingPageContent,
                );
            }
        });
    }

    _updateLandingPage(searchMade) {
        // todo: should this be managed by react?
        if (searchMade) {
            $('.landing-page-content').hide();
            $('.search-page-content').show();
            $('.findwine_filter-holder').addClass('findwine_filter-holder-search-result');
        } else {
            $('.landing-page-content').show();
            $('.search-page-content').hide();
            $('.findwine_filter-holder').removeClass('findwine_filter-holder-search-result');
        }
    }

    updateCategory(category) {
        this.setState({
            selectedCategory: category,
            selectedSubcategory: '',  // default to empty/all
        }, this.updateSearchResults);
    }

    updateSubcategory(subcategory) {
        this.setState({selectedSubcategory: subcategory}, this.updateSearchResults);
    }

    updateMinPrice(price, updateResults) {
        if (updateResults) {
          this.setState({minPrice: price}, this.updateSearchResults);
        } else {
          this.setState({minPrice: price});
        }
    }

    updateMaxPrice(price, updateResults) {
        if (updateResults) {
          this.setState({maxPrice: price}, this.updateSearchResults);
        } else {
          this.setState({maxPrice: price});
        }
    }

    updateSort(sort) {
        this.setState({selectedSort: sort}, this.updateSearchResults);
    }

    searchClicked(event) {
        event.preventDefault();
        this._updateSearchResults();
    }

    updateSearchResults() {
        if (this.state['firstSearchMade']) {
            this._updateSearchResults();
        }
    }

    _updateSearchResults() {
        let params = {
            category: this.state['selectedCategory'],
            sub_category: this.state['selectedSubcategory'],
            min_price: this.state['minPrice'],
            max_price: this.state['maxPrice'],
            sort_by: this.state['selectedSort'],
        }
        // TODO: this duplication is silly
        let queryParams = {
            selectedCategory: this.state['selectedCategory'],
            selectedSubcategory: this.state['selectedSubcategory'],
            minPrice: this.state['minPrice'],
            maxPrice: this.state['maxPrice'],
            selectedSort: this.state['selectedSort'],
        }
        if (this.state['firstSearchMade']) {
            window.history.replaceState(queryParams, 'Search Results', `/search/?${queryString.stringify(queryParams)}`)
        } else {
            // back button support for first search
            window.history.pushState(queryParams, 'Search Results', `/search/?${queryString.stringify(queryParams)}`)
        }
        params = queryString.stringify(params);
        fetch(WINE_API_URL + '?' + params).then((response) => this._updateResultsFromResponse(response));
        this.setState({firstSearchMade: true});
        this._updateLandingPage(true);
    }

    nextPage() {
        if (this.state['nextPageUrl']) {
            fetch(this.state['nextPageUrl']).then((response) => this._updateResultsFromResponse(response));
        }
    }

    prevPage() {
        if (this.state['prevPageUrl']) {
            fetch(this.state['prevPageUrl']).then((response) => this._updateResultsFromResponse(response));
        }
    }

    _updateResultsFromResponse(response) {
        if (response.ok) {
            response.json().then((responseJson) => {
                this.setState({
                    wines: responseJson.results,
                    nextPageUrl: responseJson.next,
                    prevPageUrl: responseJson.previous,
                    resultCount: responseJson.count,
                    resultPage: responseJson.page,
                    resultStart: responseJson.start,
                    resultEnd: responseJson.end,
                });
            });
        }
    }

    render() {
        let ratingsExplained = this.state.firstSearchMade ? <RatingsExplanationBar /> : '';
        let wineList = this.state.firstSearchMade ? <WineList wines={this.state.wines}/> : '';
        let paginator = this.state.firstSearchMade ? <Paginator
            nextPage={() => this.nextPage()} showNext={Boolean(this.state.nextPageUrl)}
            prevPage={() => this.prevPage()} showPrevious={Boolean(this.state.prevPageUrl)}
            count={this.state.resultCount} page={this.state.resultPage}
            start={this.state.resultStart} end={this.state.resultEnd}
        /> : '';
        return (
            <div>
                <SearchControls
                    firstSearchMade={this.state.firstSearchMade}
                    selectedCategory={this.state.selectedCategory}
                    categoryChanged={(category) => this.updateCategory(category)}
                    selectedSubcategory={this.state.selectedSubcategory}
                    subcategoryChanged={(subcategory) => this.updateSubcategory(subcategory)}
                    minPrice={this.state.minPrice}
                    minPriceChanged={(price, updateResults) => this.updateMinPrice(price, updateResults)}
                    maxPrice={this.state.maxPrice}
                    maxPriceChanged={(price, updateResults) => this.updateMaxPrice(price, updateResults)}
                    selectedSort={this.state.selectedSort}
                    sortChanged={(sort) => this.updateSort(sort)}
                    searchClicked={(event) => this.searchClicked(event)}
                    updateSearchResults={() => this.updateSearchResults()}
                />
                {ratingsExplained}
                {wineList}
                {paginator}
                <RatingsModal />
            </div>
        )
    }
}

function getCategoryChoices() {
    return CATEGORY_CHOICES;
}

function getCategoryMap() {
    // NOTE: we assume this is assigned elsewhere on the page by django
    return CATEGORY_MAP;
}

function getSubcategories(category) {
    if (category in getCategoryMap()) {
        return getCategoryMap()[category]['subcategories'];
    } else {
        return [];
    }
}

function getImagePath(category) {
    return getCategoryMap()[category]['image'];
}

function getCategoryId(category) {
    return getCategoryMap()[category]['id'];
}

function getSelectedImagePath(category) {
    return getCategoryMap()[category]['selected_image'];
}

function constructImagePath(path) {
  // assumes defined on the page.
  return `${STATIC_BASE_PATH}${path}`;
}

function getSortChoices() {
    // NOTE: these values are coupled with the API queryset!
    return [
        ['Rating', '-avg_rating'],
        ['Price', 'price'],
        ['Name', 'wine__producer__name,wine__name'],
    ];
}

ReactDOM.render(
    <SearchPage/>,
    document.getElementById('react-home')
);
