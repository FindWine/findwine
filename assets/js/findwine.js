import "babel-polyfill";
import React from 'react';
import ReactDOM from 'react-dom';
import 'whatwg-fetch';
import Select from 'react-select';

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
                            onClick={(event) => this.props.searchClicked(event)}> Search Wines <img src="static/wine/images/SVGs/arrow.svg" alt="search" className="hidden-md-up"></img>
                    </button>
                </div>
            );
        }
    }

    render() {
        return (

                <form className="search-form" role="search">
                    <div className="row d-flex align-items-end findwine_search-form">

                        <div className="col-md-3">
                            <div className="form-group category">
                                <label htmlFor="id_category" className="findwine_heading-3">Select A Category</label>

                                {/*Buttons for mobile, need to add function to change colour when clicked*/}

                                <div className="hidden-md-up findwine_button-outer">

                                    <button type="button" href="#" className="btn btn-secondary findwine_button-category" id="red">
                                        <div className="findwine_svg">
                                            <img className="findwine_button-default" src="static/wine/images/SVGs/red.svg"></img>
                                            <img className="findwine_button-active" src="static/wine/images/SVGs/red-c.svg"></img>
                                        </div>
                                        <div className="findwine_button-type">
                                            Red
                                        </div>
                                        <div className="findwine_button-bar">
                                        </div>
                                    </button>
                                    <button type="button" href="#" className="btn btn-secondary findwine_button-category" id="white">
                                        <div className="findwine_svg">
                                            <img src="static/wine/images/SVGs/white-c.svg"></img>
                                        </div>
                                        <div className="findwine_button-type">
                                            White
                                        </div>
                                        <div className="findwine_button-bar">
                                        </div>
                                    </button>
                                    <button type="button" href="#" className="btn btn-secondary findwine_button-category" id="rose">
                                        <div className="findwine_svg">
                                            <img src="static/wine/images/SVGs/rose-c.svg"></img>
                                        </div>
                                        <div className="findwine_button-type">
                                            Rosé
                                        </div>
                                        <div className="findwine_button-bar">
                                        </div>
                                    </button>
                                    <button type="button" href="#" className="btn btn-secondary findwine_button-category" id="port">
                                        <div className="findwine_svg">
                                            <img src="/static/wine/images/SVGs/port-c.svg"></img>
                                        </div>
                                        <div className="findwine_button-type">
                                            Port
                                        </div>
                                        <div className="findwine_button-bar">
                                        </div>
                                    </button>
                                    <button type="button" href="#" className="btn btn-secondary findwine_button-category" id="bubbly">
                                        <div className="findwine_svg">
                                            <img src="/static/wine/images/SVGs/bubbly-c.svg"></img>
                                        </div>
                                        <div className="findwine_button-type">
                                            Bubbly
                                        </div>
                                        <div className="findwine_button-bar">
                                        </div>
                                    </button>
                                </div>

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

                        {/*Price Range*/}

                        <div className="col-md-6">
                            <div className="form-group sub_category">
                                <label htmlFor="id_sub_category" className="findwine_heading-3"> Price Range</label>

                                {/*Slider to be added here*/}

                            </div>
                            <div class="row">
                                <div className="col-md-6">
                                    <div className="form-group min_price">
                                        <label htmlFor="id_min_price">Minimum Price</label>
                                        <input className="form-control" type="number" name="min_price"
                                               value={this.props.minPrice} min="0" required id="id_min_price"
                                               onChange={(event) => this.props.minPriceChanged(event.target.value)}
                                        />
                                    </div>
                                </div>
                                <div className="col-md-6">
                                    <div className="form-group max_price">
                                        <label htmlFor="id_max_price">Maximum Price</label>
                                        <input className="form-control" type="number" name="max_price"
                                               value={this.props.maxPrice} min="0" required id="id_max_price"
                                               onChange={(event) => this.props.maxPriceChanged(event.target.value)}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                        {this._getSortSelect()}
                    </div>
                    {this._getSearchButton()}
                </form>
        )
    }
}

class WineList extends React.Component {
    render() {
        if (this.props.wines.length > 0) {
            return (
                <table className="table">
                    <thead className="thead">
                    <tr>
                        <th>Name</th>
                        <th>Rating /10</th>
                        <th>Minimum Price</th>
                    </tr>
                    </thead>
                    <tbody>
                    {this.props.wines.map((winevintage, index) => {
                        return (
                            <tr key={index}>
                                <td scope="row">
                                    <a className="text-primary"
                                       href={winevintage.details_url}>{winevintage.wine.producer}
                                        - {winevintage.wine.name} {winevintage.year}</a></td>
                                <td>{winevintage.avg_rating}</td>
                                <td>R {winevintage.price}</td>
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

class Paginator extends React.Component {
    render() {
        // let nextButton = this.props.showNext ? `<a onClick=${(event) => this.props.nextPage()}>Next</a>` : '';
        let nextButton = this.props.showNext ?
            <a className="next-nav" onClick={(event) => this.props.nextPage()}>Next</a> : '';
        let prevButton = this.props.showPrevious ?
            <a className="prev-nav" onClick={(event) => this.props.prevPage()}>Previous</a> : '';
        return (
            <div>
                {prevButton}
                {nextButton}
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
            wines: [],
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

    updateMinPrice(price) {
        this.setState({minPrice: price}, this.updateSearchResults);
    }

    updateMaxPrice(price) {
        this.setState({maxPrice: price}, this.updateSearchResults);
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
                });
            });
        }
    }

    render() {
        let wineList = this.state.firstSearchMade ? <WineList wines={this.state.wines}/> : '';
        let paginator = this.state.firstSearchMade ? <Paginator
            nextPage={() => this.nextPage()} showNext={Boolean(this.state.nextPageUrl)}
            prevPage={() => this.prevPage()} showPrevious={Boolean(this.state.prevPageUrl)}
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
                    minPriceChanged={(price) => this.updateMinPrice(price)}
                    maxPrice={this.state.maxPrice}
                    maxPriceChanged={(price) => this.updateMaxPrice(price)}
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
        return getCategoryMap()[category];
    } else {
        return [];
    }
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
