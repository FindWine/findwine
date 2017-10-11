import "babel-polyfill";
import React from 'react';
import ReactDOM from 'react-dom';
import 'whatwg-fetch';

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
    let choices = getSubcategories(this.props.selectedCategory);
    return (
      <select className="form-control" name="sub_category" id="id_sub_category" value={this.props.selectedSubcategory}
        onChange={(event) => this.props.subcategoryChanged(event.target.value)}>
        {choices.map((category, index) => {
            return (
              <option key={index} value={category}>{category}</option>
            )
        })}
      </select>
    );
  }
}

class SearchControls extends React.Component {

  render() {
    return (
      <div>
      <h5 style={{paddingTop: '10%', paddingBottom: '5%', textAlign: 'center'}}>What wine would you like to find?</h5>
  		<form className="search-form" role="search" >
  			<div className="row d-flex align-items-end">
  				<div className="col-sm-3">
  					<div className="form-group category">
  						<label htmlFor="id_category">Category</label>
              <CategorySelect
                selectedCategory={this.props.selectedCategory}
                categoryChanged={this.props.categoryChanged}
              />
  					</div>
  				</div>
  				<div className="col-sm-3">
  					<div className="form-group sub_category">
  						<label htmlFor="id_sub_category">Type</label>
              <SubCategorySelect
                selectedCategory={this.props.selectedCategory}
                selectedSubcategory={this.props.selectedSubcategory}
                subcategoryChanged={this.props.subcategoryChanged}
              />
  					</div>
  				</div>
  				<div className="col-sm-2">
  					<div className="form-group min_price">
  						<label htmlFor="id_min_price">Minimum Price</label>
  						<input className="form-control" type="number" name="min_price" value={this.props.minPrice} min="0" required id="id_min_price"
                onChange={(event) => this.props.minPriceChanged(event.target.value)}
              />
  					</div>
  				</div>
  				<div className="col-sm-2">
  					<div className="form-group max_price">
  						<label htmlFor="id_max_price">Maximum Price</label>
  						<input className="form-control" type="number" name="max_price" value={this.props.maxPrice} min="0" required id="id_max_price"
                onChange={(event) => this.props.maxPriceChanged(event.target.value)}
              />
  					</div>
  				</div>
  				<div className="col-sm-2">
  					<button type="submit" className="btn btn-primary btn-block" style={{marginBottom: '16px', marginTop: '16px'}}
                    onClick={(event) => this.props.searchClicked(event)}>Find wine</button>
  				</div>
  			</div>
  		</form>
  	</div>
    )
  }
}

class WineList extends React.Component {
  render () {
    if (this.props.wines.length > 0) {
      return (
        <table className="table">
    			<thead className="thead">
    				<tr>
    					<th>Name</th>
    					<th>Rating /10</th>
    					<th>Minimum Price</th>
              <th>Buy</th>
    				</tr>
    			</thead>
    			<tbody>
            {this.props.wines.map((winevintage, index) => {
            return (
    				  <tr key={index}>
      				  <td scope="row">
                  <a className="text-primary" href={winevintage.details_url}>{ winevintage.wine.producer } - { winevintage.wine.name } { winevintage.year }</a></td>
      				  <td>{winevintage.avg_rating }</td>
      				  <td>R {winevintage.price}</td>
                <td><a className="text-primary" href={ winevintage.preferred_merchant_url } target="_blank">Buy</a></td>
      				</tr>
            );
          })}
    			</tbody>
  		  </table>
      );
    } else {
      return (
        <p style={{textAlign: 'center', paddingTop: '10%', marginBottom: '450px'}}>No results are available. Adjust criteria and search again.</p>
      )
    }
  }
}

class Paginator extends React.Component {
  render() {
    // let nextButton = this.props.showNext ? `<a onClick=${(event) => this.props.nextPage()}>Next</a>` : '';
    let nextButton = this.props.showNext ? <a className="next-nav" onClick={(event) => this.props.nextPage()}>Next</a> : '';
    let prevButton = this.props.showPrevious ? <a className="prev-nav" onClick={(event) => this.props.prevPage()}>Previous</a> : '';
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
    const subcategory = getSubcategories(category)[0];
    this.state = {
      selectedCategory: category,
      selectedSubcategory: subcategory,
      minPrice: 0,
      maxPrice: 500,
      wines: [],
      nextPageUrl: null,
      prevPageUrl: null,
    }
  }

  updateCategory(category) {
    this.setState({
      selectedCategory: category,
      selectedSubcategory: getSubcategories(category)[0],  // default to first
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

  searchClicked(event) {
    event.preventDefault();
    this.updateSearchResults();
  }

  updateSearchResults() {
    let params = {
      category: this.state['selectedCategory'],
      sub_category: this.state['selectedSubcategory'],
      min_price: this.state['minPrice'],
      max_price: this.state['maxPrice'],
    }
    // TODO: assumes jquery on page.
    params = $.param(params);
    fetch(WINE_API_URL + '?' + params).then((response) => this._updateResultsFromResponse(response));
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
    if(response.ok) {
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
    return (
      <div className="container">
        <SearchControls
          selectedCategory={this.state.selectedCategory}
          categoryChanged={(category) => this.updateCategory(category)}
          selectedSubcategory={this.state.selectedSubcategory}
          subcategoryChanged={(subcategory) => this.updateSubcategory(subcategory)}
          minPrice={this.state.minPrice}
          minPriceChanged={(price) => this.updateMinPrice(price)}
          maxPrice={this.state.maxPrice}
          maxPriceChanged={(price) => this.updateMaxPrice(price)}
          searchClicked={(event) => this.searchClicked(event)}
          updateSearchResults={() => this.updateSearchResults()}
        />
        <WineList
          wines={this.state.wines}
        />
        <Paginator
          nextPage={() => this.nextPage()} showNext={Boolean(this.state.nextPageUrl)}
          prevPage={() => this.prevPage()} showPrevious={Boolean(this.state.prevPageUrl)}
        />
      </div>
    )
  }
}

ReactDOM.render(

  <SearchPage />,
  document.getElementById('react-home')
);

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
