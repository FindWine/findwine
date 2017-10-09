import React from 'react';
import ReactDOM from 'react-dom';


class CategorySelect extends React.Component {
  constructor() {
    super();
    this.state = {
      choices: {}
    }
  }

  render() {
    return (
      <select name="category" id="id_category"
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
      <select name="sub_category" id="id_sub_category"
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
  		<form className="search-form" role="search" action="/search/" method="get">
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
                subcategoryChanged={this.props.subcategoryChanged}
              />
  					</div>
  				</div>
  				<div className="col-sm-2">
  					<div className="form-group min_price">
  						<label htmlFor="id_min_price">Minimum Price</label>
  						<input className="form-control" type="number" name="min_price" value="0" min="0" required id="id_min_price" />
  					</div>
  				</div>
  				<div className="col-sm-2">
  					<div className="form-group max_price">
  						<label htmlFor="id_max_price">Maximum Price</label>
  						<input className="form-control" type="number" name="max_price" value="500" min="0" required id="id_max_price" />
  					</div>
  				</div>
  				<div className="col-sm-2">
  					<button type="submit" className="btn btn-primary btn-block" style={{marginBottom: '16px', marginTop: '16px'}}>Find wine</button>
  				</div>
  			</div>
  		</form>
  	</div>
    )
  }
}
class SearchPage extends React.Component {
  constructor() {
    super();
    this.state = {
      selectedCategory: getCategoryChoices()[0]  // select first category
    }
  }

  updateCategory(category) {
    this.setState({selectedCategory: category});
  }
  updateSubcategory(subcategory) {
    this.setState({selectedSubcategory: subcategory});
  }
  render() {
    return (
      <div className="container">
        <SearchControls
          selectedCategory={this.state.selectedCategory}
          categoryChanged={(category) => this.updateCategory(category)}
          selectedSubcategory={this.state.selectedCategory}
          subcategoryChanged={(subcategory) => this.updateSubcategory(subcategory)}
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
