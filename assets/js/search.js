import React from 'react';
import ReactDOM from 'react-dom';
import 'whatwg-fetch';
import {WineList, Paginator, constructImagePath} from "./shared";

const queryString = require('query-string');

// todo: figure out how to django-ize these
const SEARCH_API_URL = '/api/search/';

class SearchByNameControl extends React.Component {
  render() {
    return (
      <div className="findwine_search-name">
        <input type="text" id="search" placeholder="Search wine or winery" className="form-control mr-sm-2 findwine_search-field"
               value={this.props.searchText}
               onChange={(e) => this.props.searchTextChanged(e.target.value)}
               onKeyPress={(e) => this.handleKeyPress(e.key)}
        />
        <button className="btn btn-outline-success my-2 my-sm-0 findwine_search-button"
                onClick={() => this.props.doSearch()}> <img src={constructImagePath('wine/images/SVGs/search.svg')} alt="search"></img></button>
      </div>
    );
  }

  handleKeyPress(key) {
    if (key === 'Enter') {
      this.props.doSearch();
    } else {
      // console.log('not enter', key);
    }
  }
}

class SearchByNamePage extends React.Component {
  constructor() {
    super();
    this.state = {
      searchText: '',
      // results / pagination
      wines: [],
      resultCount: 0,
      resultPage: 1,
      resultStart: 1,
      resultEnd: 10,
      nextPageUrl: null,
      prevPageUrl: null,
      firstSearchMade: false,
      isLoading: false,
    }
  }

  render() {
    let showPaginator = (this.state.wines.length);
    let paginator = showPaginator ? <Paginator
      nextPage={() => this.nextPage()} showNext={Boolean(this.state.nextPageUrl)}
      prevPage={() => this.prevPage()} showPrevious={Boolean(this.state.prevPageUrl)}
      count={this.state.resultCount} page={this.state.resultPage}
      start={this.state.resultStart} end={this.state.resultEnd}
    /> : '';

    return (
      <div>
        <nav className="navbar navbar-toggleable-md navbar-light bg-faded navbar-new search-page-content"
             style={{display: 'none'}} id="top">
          <div className="container findwine_nav--menu">
            <button className="navbar-toggler" type="button" data-toggle="modal" data-target="#exampleModalLong">
          <span>
            <img src={ constructImagePath('wine/images/SVGs/menu-black.svg') } className="findwine_menu-button"></img>
          </span>
            </button>

            <div className="collapse navbar-collapse" id="navbarSupportedContent">
              <ul className="navbar-nav mr-auto">
                <li className="nav-item active nav-item-new">
                  <a className="nav-link nav-link-new" href="/search">Home <span
                    className="sr-only">(current)</span></a>
                </li>
                <li className="nav-item nav-item-new">
                  <a className="nav-link nav-link-new" href="/about">About</a>
                </li>
              </ul>
              <div className="findwine_search-field-holder">
                <SearchByNameControl searchText={this.state.searchText}
                                     searchTextChanged={(text) => this.searchTextChanged(text)}
                                     doSearch={() => this.doSearch()}
                />
              </div>
            </div>
          </div>
          <div className="findwine_nav-logo search-page-content">
            <a href="/search">
              <img src={ constructImagePath('wine/images/SVGs/logo-black.svg') }
                   className="d-inline-block align-top findwine_nav-logo-icon" alt="FindWine"></img>
            </a>
          </div>
        </nav>
        <div className="container">
           <div className="findwine_search-results-holder">
             <WineList wines={this.state.wines} isLoading={this.state.isLoading}/>
            {paginator}
          </div>
        </div>
      </div>
    )
  }

  componentDidMount() {
    let queryParams = queryString.parse(location.search);
    if (Object.keys(queryParams).length && queryParams['q']) {
      this.setState({
        searchText: queryParams['q']
      }, this.doSearch);
    }
  }

  searchTextChanged(text) {
    this.setState({
      searchText: text
    });
  }

  doSearch() {
    let params = queryString.stringify({q: this.state.searchText});
    fetch(SEARCH_API_URL + '?' + params).then((response) => this._updateResultsFromResponse(response));
    window.history.replaceState(params, 'Search Results', `/search-by-name/?${params}`)

    return(
      <div className="container">
        <WineList wines={this.state.wines} isLoading={this.state.isLoading}/>
      </div>
    )
  }

  _updateResultsFromResponse(response) {
    if (response.ok) {
      response.json().then((responseJson) => {
        // console.log(responseJson.results);
        this.setState({
          wines: responseJson.results,
          nextPageUrl: responseJson.next,
          prevPageUrl: responseJson.previous,
          resultCount: responseJson.count,
          resultPage: responseJson.page,
          resultStart: responseJson.start,
          resultEnd: responseJson.end,
          isLoading: false,
        });
      });
    }
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

}

ReactDOM.render(
  <SearchByNamePage/>,
  document.getElementById('search-bar')
);
