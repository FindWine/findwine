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
        return (
            <select className="form-control" name="category" id="id_category"
                    value={this.props.selectedCategory}
                    onChange={(event) => this.props.categoryChanged(event.target.value)}>
                {getCategoryChoices().map((category, index) => {
                    return (
                        <option key={index} value={category}>{category}</option>
                    )
                })}
            </select>
        );
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
                placeholder='Show All'
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
                            style={{marginBottom: '16px', marginTop: '16px'}}
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

    render() {
        return (
                <form className="search-form" role="search">
                    <div className="row d-flex align-items-end findwine_search-form">

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
                                <label htmlFor="id_sub_category" className="findwine_heading-3"> Select Type(s)</label>
                                <SubCategorySelect
                                    selectedCategory={this.props.selectedCategory}
                                    selectedSubcategory={this.props.selectedSubcategory}
                                    subcategoryChanged={this.props.subcategoryChanged}
                                />
                            </div>
                        </div>

                        <div className="col-xs-12 col-md-6">
                            <div className="col-xs-12 col-md-3" style={{padding: '0px', display:'inline-block'}}>
                                <div className="form-group sub_category">
                                    <label htmlFor="id_sub_category" className="findwine_heading-3"> Price Range </label>
                                </div>
                            </div>
                            {/*Slider - mobile layout slider appears above max and min price*/}
                            <div className="col-xs-12 hidden-md-up">
                                {this.getSlider()}
                            </div>
                            <div className="col-xs-6 col-md-4 findwine_price-input">
                               <div className="form-group min_price">
                                   R <input className="form-control" type="number" name="min_price"
                                          value={this.props.minPrice} min="0" required id="id_min_price"
                                          onChange={(event) => this.props.minPriceChanged(event.target.value, true)}
                                   />
                               </div>
                               <div className="price-range"> TO </div>
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
        )
    }
}

// This should be the Search results page that opens a new window when you click on search. Once this is created I will drop in the custom nav, filter bar and info bar. If I try to include it after return ( the page breaks.

class WineList extends React.Component {
    render() {
        if (this.props.wines.length > 0) {
            return (

                <table className="table table-responsive table-sm">
                    <tbody>
                    {this.props.wines.map((winevintage, index) => {
                        return (
                            <tr key={index} className="findwine_search-results">
                                <td className="findwine_search-result--table">
                                  <div className="findwine_vintage-rating--box findwine_vintage-rating"> {winevintage.avg_rating} </div>
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
                                </td>
                            </tr>
                        );
                    })}
                    </tbody>
                </table>
            );
        } else {
            return (
                <p style={{textAlign: 'center', paddingTop: '10%', marginBottom: '450px'}}>No results are available.
                    Adjust criteria and search again.</p>
            )
        }
    }
}

/**
 *  <div class="findwine_merchant-currency"> R </div> <div class="findwine_merchant-price"> {{ merchantwine.price }} </div>
 */

class Paginator extends React.Component {
    render() {
        // let nextButton = this.props.showNext ? `<a onClick=${(event) => this.props.nextPage()}>Next</a>` : '';
        let nextButton = this.props.showNext ?
            <a className="btn findwine_search-next--button" onClick={(event) => this.props.nextPage()}><img src={constructImagePath('wine/images/SVGs/arrow-right.svg')} alt="Next"></img></a> : <a className="btn findwine_search-next--button-inactive" onClick={(event) => this.props.nextPage()}><img src={constructImagePath('wine/images/SVGs/arrow-right-greyLight.svg')} alt="Next"></img></a>;
        let prevButton = this.props.showPrevious ?
            <a className="btn findwine_search-next--button findwine_search-next--button-left" onClick={(event) => this.props.prevPage()}><img src={constructImagePath('wine/images/SVGs/arrow-left.svg')} alt="Previous"></img></a> : <a className="btn findwine_search-next--button-inactive" onClick={(event) => this.props.nextPage()}><img src={constructImagePath('wine/images/SVGs/arrow-left-grey.svg')} alt="Next"></img></a>;

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
            selectedCategory: category,
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
            this.setState(queryParams, this._updateSearchResults);
        }
        // there might be a better way to do this
        // clear search results on back button press back to home page
        var self = this;
        $(window).on('popstate', function (e) {
            if (location.pathname === '/') {
                self.setState({
                    'firstSearchMade': false,
                });
            }
        });
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
        let wineList = this.state.firstSearchMade ? <WineList wines={this.state.wines}/> : '';
        let paginator = this.state.firstSearchMade ? <Paginator
            nextPage={() => this.nextPage()} showNext={Boolean(this.state.nextPageUrl)}
            prevPage={() => this.prevPage()} showPrevious={Boolean(this.state.prevPageUrl)}
            count={this.state.resultCount} page={this.state.resultPage}
            start={this.state.resultStart} end={this.state.resultEnd}
        /> : '';
        return (
            <div className="container">
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
                {wineList}
                {paginator}
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
