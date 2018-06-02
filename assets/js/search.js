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
        <button className="btn btn-outline-success my-2 my-sm-0 findwine_search-button" id="closeModal"
                onClick={() => {this.props.doSearch(), this.closeModal()}}>
          <img src={constructImagePath('wine/images/SVGs/search.svg')} alt="search"></img>
        </button>
      </div>
    );
  }

  handleKeyPress(key) {
    if (key === 'Enter') {
      this.props.doSearch();
  } else {
    }
  }

  closeModal() {
    $('#exampleModalLong').hide()
    $('body').removeClass('modal-open')
    $('.modal-backdrop').removeClass('modal-backdrop')
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
        <nav className="navbar navbar-toggleable-md navbar-light bg-faded navbar-new"
             id="top">
          <div className="container findwine_nav--menu">
            <button className="navbar-toggler" type="button" data-toggle="modal" data-target="#exampleModalLong">
          <span>
            <img src={ constructImagePath('wine/images/SVGs/menu-black.svg') } className="findwine_menu-button"></img>
          </span>
            </button>

            <div className="collapse navbar-collapse" id="navbarSupportedContent">
              <ul className="navbar-nav mr-auto">
                <li className="nav-item active nav-item-new">
                  <a className="nav-link nav-link-new" href="/search">Home
                  </a>
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
          <div className="findwine_nav-logo">
            <a href="/">
              <img src={ constructImagePath('wine/images/SVGs/logo-black.svg') }
                   className="d-inline-block align-top findwine_nav-logo-icon" alt="FindWine"></img>
            </a>
          </div>
          <div className="modal left fade" id="exampleModalLong" tabIndex="-1" role="dialog"
               aria-labelledby="exampleModalLongTitle" aria-hidden="true">
            <div className="modal-dialog findwine_modal-nav" role="document">
              <div className="modal-content findwine_modal-nav-content">
                <div className="modal-header findwine_modal-nav-header">
                  <button type="button" className="close findwine_modal-nav-close" data-dismiss="modal"
                          aria-label="Close">
                    <span aria-hidden="true">
                      <img src={ constructImagePath('wine/images/SVGs/close.svg') }
                           className="findwine_menu-button"></img></span>
                  </button>
                </div>
                <div className="modal-body">
                  <ul className="navbar-nav mr-auto">
                    <li className="nav-item">
                      <a className="nav-link findwine_modal-nav-link nav-link-home" href="/search">Home
                        <span className="sr-only" id="home">(current)</span>
                      </a>
                    </li>
                    <li className="nav-item">
                      <a className="nav-link findwine_modal-nav-link" href="/about">About</a>
                    </li>
                    <li className="nav-item">
                      <div className="findwine_search-field-holder">
                        <SearchByNameControl searchText={this.state.searchText}
                                             searchTextChanged={(text) => this.searchTextChanged(text)}
                                             doSearch={() => this.doSearch()}
                        />
                      </div>
                    </li>
                  </ul>
                </div>
                <div className="modal-footer findwine_modal-nav-footer">
                  <div className="findwine_modal-nav-footer-links">
                    <ul className="findwine_modal-nav-footer-links-ul">
                      <li className="findwine_modal-nav-footer-links-li">
                        <a className="findwine_modal-nav-footer-link" href="/contact">Contact Us</a>
                      </li>
                      <li className="findwine_modal-nav-footer-links-li">
                        <a className="findwine_modal-nav-footer-link" href="/terms">Privacy & Terms</a>
                      </li>
                    </ul>
                  </div>
                  <div className="findwine_modal-nav-footer-social">
                    <a href="https://www.instagram.com/findwinesa/" target="_blank"
                       className="findwine_footer--flex-right">
                      <img src={ constructImagePath('wine/images/SVGs/instagram-dark.svg') }
                           className="findwine_modal-nav-footer-icon"></img>
                    </a>
                    <a href="https://twitter.com/FindWineSA" target="_blank" className="findwine_footer--flex-right">
                      <img src={ constructImagePath('wine/images/SVGs/twitter-dark.svg') }
                           className="findwine_modal-nav-footer-icon"></img>
                    </a>
                    <a href="https://www.facebook.com/FindWineSA/" target="_blank"
                       className="findwine_footer--flex-right">
                      <img src={ constructImagePath('wine/images/SVGs/facebook-dark.svg') }
                           className="findwine_modal-nav-footer-icon"></img>
                    </a>
                  </div>
                </div>
              </div>
            </div>
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
    window.history.replaceState(params, 'Search Results', `/search-by-name/?${params}`);

    return(
      <div className="container">
        <WineList wines={this.state.wines} isLoading={this.state.isLoading}/>
      </div>
    )
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
