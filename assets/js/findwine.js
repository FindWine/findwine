import "babel-polyfill";
import React from 'react';
import ReactDOM from 'react-dom';
import 'whatwg-fetch';
import Select from 'react-select';
require('rc-slider/assets/index.css');
import 'react-select/dist/react-select.css';
import Slider, {Range} from 'rc-slider';
import {constructImagePath, WineList, Paginator} from "./shared";

const queryString = require('query-string');

// todo: figure out how to django-ize these
const WINE_API_URL = '/api/wine-vintages/';

const DEFAULT_MAX_PRICE = 150;
const MAX_PRICE = 2000;

class CategoryOption extends React.Component {
    // adapted from https://github.com/JedWatson/react-select/blob/master/examples/src/components/CustomComponents.js
    handleMouseDown (event) {
      event.preventDefault();
      event.stopPropagation();
      this.props.onSelect(this.props.option, event);
    }
    handleMouseEnter (event) {
      this.props.onFocus(this.props.option, event);
    }
    handleMouseMove (event) {
      if (this.props.isFocused) return;
      this.props.onFocus(this.props.option, event);
    }
    render () {
      // console.log('props', this.props);
      const image = this.props.isSelected ? getSelectedImagePath(this.props.option.value) : getImagePath(this.props.option.value);
      return (
        <div className={this.props.className}
          onMouseDown={(event) => this.handleMouseDown(event)}
          onMouseEnter={(event) => this.handleMouseEnter(event)}
          onMouseMove={(event) => this.handleMouseMove(event)}
          title={this.props.option.title}>
            <img src={image} className="findwine_select-svg"></img>
            {this.props.children}
        </div>
      );
    }
}

class CategoryValue  extends React.Component {
  render () {
    const image = getSelectedImagePath(this.props.value.value);
		return (
      <div className="Select-value" title={this.props.value.title}>
        <span className="Select-value-label">
          {this.props.children}
        </span>
      </div>
    );
  }
}

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
        searchable={false}
        clearable={false}
        optionComponent={CategoryOption}
        valueComponent={CategoryValue}
      />
    )
  }
}

class CategorySelectMobile extends React.Component {
  render() {
    return (
      <div className="hidden-lg-up findwine_button-outer" value={this.props.selectedCategory}>
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

class SubCategoryOption extends React.Component {
  // also adapted from https://github.com/JedWatson/react-select/blob/master/examples/src/components/CustomComponents.js
  handleMouseDown (event) {
    event.preventDefault();
    event.stopPropagation();
    this.props.onSelect(this.props.option, event);
  }
  handleMouseEnter (event) {
    this.props.onFocus(this.props.option, event);
  }
  handleMouseMove (event) {
    if (this.props.isFocused) return;
    this.props.onFocus(this.props.option, event);
  }
  render () {
    const image = (
      this.props.isSelected ?
        constructImagePath('wine/images/SVGs/tick-box-fill.svg') :
        constructImagePath('wine/images/SVGs/tick-box.svg')
    );
    return (
      <div className={this.props.className}
        onMouseDown={(event) => this.handleMouseDown(event)}
        onMouseEnter={(event) => this.handleMouseEnter(event)}
        onMouseMove={(event) => this.handleMouseMove(event)}
        title={this.props.option.title}>
            <div className="findwine_select-box-height">
              <img src={image} className="findwine_select-box"></img>
            </div>
            <div className="findwine_subcategory-option"> {this.props.children} </div>
      </div>
    );
  }
}

class CustomSelect extends Select {
  renderValue (valueArray, isOpen) {
    if (this.props.multi && valueArray.length) {
      if (valueArray.length === 1) {
        return valueArray[0].label;
      } else {
        return "Multiple";
      }
    }
    else {
      return super.renderValue(valueArray, isOpen);
    }
  }
}

class SubCategorySelect extends React.Component {
  render() {
    let choices = getSubcategories(this.props.selectedCategory).map((choice) => {
      return {'value': choice, 'label': choice}
    });
    return (
      <CustomSelect
        value={this.props.selectedSubcategory}
        options={choices}
        onChange={(value) => this.props.subcategoryChanged(value)}
        multi={true}
        simpleValue={true}
        searchable={false}
        clearable={false}
        autosize={false}
        removeSelected={false}
        closeOnSelect={false}
        placeholder='All'
        optionComponent={SubCategoryOption}
      />
    )
  }
}

class SortSelect extends React.Component {
  render() {
    let choices = getSortChoices().map((sortChoice, index) => {
      return {'value': sortChoice[1], 'label': sortChoice[0]};
    });
    return (
      <Select
        value={this.props.selectedSort}
        options={choices}
        onChange={(value) => this.props.sortChanged(value)}
        multi={false}
        simpleValue={true}
        searchable={false}
        clearable={false}
      />
    );
  }
}

class SearchControls extends React.Component {
  _getSortSelect() {
    if (this.props.firstSearchMade) {
      return (
        <div className="col-12">
          <div className="form-group">
            <label htmlFor="id_sort" className="findwine_heading-3">Sort by</label>
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
        <div className="col-md-6 offset-md-3 col-lg-12 offset-lg-0 findwine_button-outer">
          <button type="submit" className="btn btn-primary btn-block findwine_button" href="#modal"
                  onClick={(event) => this.props.searchClicked(event)}>
            SEARCH WINES
            <img src={constructImagePath('wine/images/SVGs/arrow.svg')} alt="search" className="findwine_button-image"></img>
          </button>
        </div>
      );
    }
  }

  _getSearchButtonFilter() {
    if (this.props.firstSearchMade) {
      return (
        <div className="col-md-8 offset-md-2 col-lg-12 offset-lg-0 findwine_button-outer">
          <button type="button" className="btn btn-primary btn-block findwine_button"
                  onClick={(e) => this._doMobileSearch()}>
            SEARCH WINES
            <img src={constructImagePath('wine/images/SVGs/arrow.svg')} alt="search" className="hidden-lg-up findwine_button-image"></img>
          </button>
        </div>
      );
    }
  }

  _doMobileSearch() {
      this.props.setExpanded(false);
      this.props.searchClicked();
  }

  getSlider() {
    const minPriceInt = parseInt(this.props.minPrice) || 0;
    const maxPriceInt = parseInt(this.props.maxPrice) || DEFAULT_MAX_PRICE;
    return (
      <Range
        defaultValue={[0,DEFAULT_MAX_PRICE]}
        max={MAX_PRICE}
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
    if (this.props.firstSearchMade && this.props.isExpanded) {
      return (
        <button className="findwine_filters-expand-button findwine_filters-close-button"
                type="button" href="#modal"
                style={{outline: 'none', border:'none', background: "none"}}>
          X
        </button>
      )
    }
  }

  renderControls() {
    return (
      <form className="search-form" role="search">
        {this.renderCollapsedControlsOpen()}
        <div className="align-items-start findwine_search-form">
          <div className="form-group category">
            <label htmlFor="id_category" className="findwine_heading-3">Select wine</label>
              <CategorySelectMobile
                selectedCategory={this.props.selectedCategory}
                categoryChanged={this.props.categoryChanged}
              />
            <div className="hidden-md-down">
              <CategorySelect
                  selectedCategory={this.props.selectedCategory}
                  categoryChanged={this.props.categoryChanged}
              />
            </div>
          </div>
        <div className="form-group sub_category">
          <label htmlFor="id_sub_category" className="findwine_heading-3"> Select type(s)</label>
          <SubCategorySelect
              selectedCategory={this.props.selectedCategory}
              selectedSubcategory={this.props.selectedSubcategory}
              subcategoryChanged={this.props.subcategoryChanged}
          />
        </div>
        <div className="findwine_subcategory-row">
          <div className="col-xs-12 col-lg-4 findwine_subcategory" >
            <div className="form-group sub_category">
              <label htmlFor="id_sub_category" className="findwine_heading-3"> Price range </label>
            </div>
          </div>
          <div className="col-xs-12 hidden-lg-up">
              {this.getSlider()}
          </div>
          <div className="col-xs-6 col-lg-8 findwine_price-input">
             <div className="form-group min_price">
               R <input className="form-control findwine_price" type="text" name="min_price"
                        value={this.props.minPrice} min="0" required id="id_min_price"
                        onChange={(event) => this.props.minPriceChanged(event.target.value, true)}
               />
             </div>
             <div className="price-range hidden-lg-up"> TO </div>
            <div className="price-range hidden-md-down"> - </div>
             <div className="form-group max_price">
               R  <input className="form-control findwine_price" type="text" name="max_price"
                         value={this.props.maxPrice} min="0" required id="id_max_price"
                         onChange={(event) => this.props.maxPriceChanged(event.target.value, true)}
              />
             </div>
            </div>
            <div className="col-lg-12 hidden-md-down">
               {this.getSlider()}
            </div>
          </div>
          {this._getSortSelect()}
        </div>
        {this._getSearchButton()}
        {this._getSearchButtonFilter()}
      </form>
    );
  }

  renderCollapsedControlsDesktop(){
    return(
      <form className="search-form-collapsed" role="search">
        {this.renderCollapsedControlsOpen()}
        <div className="findwine_filter-collapse-left">
          <div className="d-flex align-items-start findwine_search-form-collapsed">
            <div className="form-group category findwine_filter-collapse-category">
              <label htmlFor="id_category" className="findwine_heading-3">Select wine</label>
              <div className="findwine_select-collapse">
                <CategorySelect
                  style={{maxWidth: '220px'}}
                  selectedCategory={this.props.selectedCategory}
                  categoryChanged={this.props.categoryChanged}
                />
              </div>
            </div>
            <div className="form-group sub_category findwine_filter-collapse-category">
              <label htmlFor="id_sub_category" className="findwine_heading-3"> Select type(s)</label>
              <div className="findwine_select-collapse">
                <SubCategorySelect
                  selectedCategory={this.props.selectedCategory}
                  selectedSubcategory={this.props.selectedSubcategory}
                  subcategoryChanged={this.props.subcategoryChanged}
                />
              </div>
            </div>
            <div className="findwine_subcategory-row findwine_filter-collapse-category-price">
              <div className="findwine_subcategory findwine_subcategory-collapse" >
                <div className="form-group sub_category-collapse">
                  <label htmlFor="id_sub_category" className="findwine_heading-3"> Price range </label>
                </div>
              </div>
              <div className="findwine_price-input-collapse">
                <div className="form-group min_price">
                  R <input className="form-control findwine_price" type="text" name="min_price"
                           value={this.props.minPrice} min="0" required id="id_min_price"
                           onChange={(event) => this.props.minPriceChanged(event.target.value, true)}
                />
                </div>
                <div className="price-range-collapse"> - </div>
                <div className="form-group max_price">
                  R  <input className="form-control findwine_price" type="text" name="max_price"
                            value={this.props.maxPrice} min="0" required id="id_max_price"
                            onChange={(event) => this.props.maxPriceChanged(event.target.value, true)}
                />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="findwine_filter-collapse-right">
          <div className="findwine_filter-collapse-category findwine_filter-collapse-category-align">
          {this._getSortSelect()}
          </div>
        </div>
      </form>
    );
  }

  renderCollapsedControls() {
    return (
      // This is for mobile and tablet - collapsed
      <div className="findwine_filters-collapsed" onClick={() => this.props.setExpanded(true)}>
        <div className="findwine_filters-icon">
          <img src={ constructImagePath('wine/images/SVGs/filter.svg')} className="findwine_filters-filter-icon" />
        </div>
        <div className="findwine_filters-heading">
          Filters
        </div>
        <div className="findwine_filters-expand">
          <button className="findwine_filters-expand-button" type="button"
                  style={{outline: 'none', border:'none', background: "none"}}>
            <img src={ constructImagePath('wine/images/SVGs/arrow-down.svg') } className="findwine_filters-expand-arrow" />
          </button>
        </div>
      </div>
    );
  }

  renderCollapsedControlsOpen() {
    if (this.props.firstSearchMade && this.props.isExpanded) {
      return (
        <div className="findwine_filters-collapsed-filter-open" onClick={() => this.props.setExpanded(false)}>
          <div className="findwine_filters-icon">
            <img src={constructImagePath('wine/images/SVGs/filter.svg')} className="findwine_filters-filter-icon"/>
          </div>
          <div className="findwine_filters-heading-open">
            Filters
          </div>
          <div className="findwine_filters-expand-open">
            {this.renderCollapseButton()}
          </div>
        </div>
      );
    }
  }

  showSearchControls() {
    return !this.props.firstSearchMade || this.props.isExpanded;
  }

  render() {
    if (this.showSearchControls()) {
      return this.renderControls();
    } else {
      if (isMobile()) {
        return this.renderCollapsedControls();
      } else {
        return this.renderCollapsedControlsDesktop();
      }
    }
  }
}

class RatingsExplanationBar extends React.Component {
    render () {
      return (
        <div className="findwine_ratings-explained--container">
          <div className="findwine_ratings-heading" data-toggle="modal" data-target="#ratingsExplained">
              Ratings explained
          </div>
          <button type="button" className="findwine_ratings-info" style={{outline: 'none', border:'none', background: "none"}}
                  data-toggle="modal" data-target="#ratingsExplained">
            <img src={ constructImagePath('wine/images/SVGs/info.svg') } className="findwine_ratings-info-icon" />
          </button>
        </div>
      );
    }
}

class RatingsModal extends React.Component {
  render() {
    return (
      <div className="modal fade" id="ratingsExplained" tabIndex="-1" role="dialog" aria-labelledby="ratingsExplainedLabel" aria-hidden="true">
        <div className="modal-dialog" role="document">
          <div className="modal-content">
            <div className="modal-body findwine_modal">
              <div className="findwine_modal-ratings">
                <img src={ constructImagePath('wine/images/SVGs/ratings.svg') } className="findwine_modal-ratings-icon" />
              </div>
              <div className="findwine_modal-heading">
                Ratings Explained
              </div>
              <div className="findwine_modal-content">
                Our smart ratings system calculates a unique score for each wine based on
                the awards they’ve won and the prestige of the award body. Scores fall
                between 0 and 10, with 10 being the highest rating a wine can receive.
              </div>
            </div>
            <div className="modal-footer findwine_modal-footer">
              <button type="button" className="btn btn-secondary findwine_modal-button" data-dismiss="modal">Got it</button>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

class SearchPage extends React.Component {
  constructor() {
    super();
    // initialize with first category / subcategory selected
    const category = getCategoryChoices()[0];
    this.state = {
        selectedCategory: category,
        selectedSubcategory: '',
        minPrice: 0,
        maxPrice: DEFAULT_MAX_PRICE,
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
        searchControlsExpanded: false,
        isLoading: false,
    }
  }

    componentDidMount() {
      let queryParams = queryString.parse(location.search);
      if (Object.keys(queryParams).length && queryParams['selectedCategory']) {
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
            $('#search-bar').removeClass('findwine_home');
        } else {
            $('.landing-page-content').show();
            $('.search-page-content').hide();
            $('.findwine_filter-holder').removeClass('findwine_filter-holder-search-result');
            $('#search-bar').addClass('findwine_home');
        }
    }

    updateCategory(category) {
        this.setState({
            selectedCategory: category,
            selectedSubcategory: '',  // default to empty/all
            resultPage: 1,  // have to reset page on every change
        }, this.updateSearchResults);
    }

    updateSubcategory(subcategory) {
        this.setState({selectedSubcategory: subcategory, resultPage: 1}, this.updateSearchResults);
    }

    updateMinPrice(price, updateResults) {
        if (updateResults) {
          this.setState({minPrice: price, resultPage: 1}, this.updateSearchResults);
        } else {
          this.setState({minPrice: price});
        }
    }

    updateMaxPrice(price, updateResults) {
        if (updateResults) {
          this.setState({maxPrice: price, resultPage: 1}, this.updateSearchResults);
        } else {
          this.setState({maxPrice: price});
        }
    }

    updateSort(sort) {
        this.setState({selectedSort: sort, resultPage: 1}, this.updateSearchResults);
    }

    searchClicked(event) {
        if (event) {
            event.preventDefault();
        }
        this._updateSearchResults();
    }

    updateSearchResults() {
        if (this.state['firstSearchMade'] && !this.state['searchControlsExpanded']) {
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
            page: this.state['resultPage'],
        }
        params = queryString.stringify(params);
        let addToHistory = !this.state.firstSearchMade;
        fetch(WINE_API_URL + '?' + params).then((response) => this._updateResultsFromResponse(response, addToHistory));
        this.setState({firstSearchMade: true, isLoading: true});
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

    _updateUrl(addToHistory) {
        // TODO: this duplication is silly
        let queryParams = {
            selectedCategory: this.state['selectedCategory'],
            selectedSubcategory: this.state['selectedSubcategory'],
            minPrice: this.state['minPrice'],
            maxPrice: this.state['maxPrice'],
            selectedSort: this.state['selectedSort'],
            resultPage: this.state['resultPage']
        }
        if (addToHistory) {
            // back button support for first search
            window.history.pushState(queryParams, 'Search Results', `/search/?${queryString.stringify(queryParams)}`)
        } else {
            window.history.replaceState(queryParams, 'Search Results', `/search/?${queryString.stringify(queryParams)}`)
        }
    }

    _updateResultsFromResponse(response, addToHistory) {
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
            isLoading: false,
          }, () => this._updateUrl(addToHistory));
        });
      }
    }

    render() {
      const mobileFiltersOpen = isMobile() && this.state.searchControlsExpanded
      const showWineList = this.state.firstSearchMade && !mobileFiltersOpen;
      let ratingsExplained = showWineList ? <RatingsExplanationBar /> : '';
      let wineList = showWineList ? <WineList wines={this.state.wines} isLoading={this.state.isLoading}/> : '';
      let showPaginator = (showWineList && this.state.wines.length);
      let paginator = showPaginator ? <Paginator
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
            isExpanded={this.state.searchControlsExpanded}
            setExpanded={(expanded) => this.setState({'searchControlsExpanded': expanded})}
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

function getSortChoices() {
    // NOTE: these values are coupled with the API queryset!
    return [
        ['Rating', '-avg_rating'],
        ['Price', 'price'],
        ['Name', 'wine__producer__name,wine__name'],
    ];
}

function loader() {
  if (this.props.wines.length > 0) {
    document.getElementById('loader').style.display='block';
    setTimeout("hide()", 500);
  }
}

function hide() {
  document.getElementById("loader").style.display="none";
}

function isMobile() {
  return window.innerWidth < 992;
}

ReactDOM.render(
    <SearchPage/>,
    document.getElementById('react-home')
);
