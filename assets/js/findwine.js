import "babel-polyfill";
import React from 'react';
import ReactDOM from 'react-dom';
import 'whatwg-fetch';

// todo: figure out how to django-ize these
const WINE_API_URL = '/api/wine-vintages/';

class CategorySelect extends React.Component {
  constructor() {
    super();
    this.state = {
      choices: {}
    }
  }

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
        <table className="table" style={{marginBottom: '50px'}}>
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
    }
  }

  updateCategory(category) {
    this.setState({
      selectedCategory: category,
      selectedSubcategory: getSubcategories(category)[0],  // default to first
    });
  }

  updateSubcategory(subcategory) {
    this.setState({selectedSubcategory: subcategory});
  }

  updateMinPrice(price) {
    this.setState({minPrice: price});
  }

  updateMaxPrice(price) {
    this.setState({maxPrice: price});
  }

  searchClicked(event) {
    event.preventDefault();
    console.log('search clicked!');
    fetch(WINE_API_URL).then((response) => {
      if(response.ok) {
        response.json().then((responseJson) => {
          this.setState({
            wines: responseJson
          });
        });
      }
    });

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
        />
        <WineList
          wines={this.state.wines}
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
