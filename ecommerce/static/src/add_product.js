
let category = document.getElementById("category");
category.onchange = () => {
  cate = category.value;
  fetch("/products/new" + cate).then(function(response) {
    response.json().then(function(data) {
      let optionHTML = "";
      console.log(data);
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  let category = document.getElementById('category');
  category.onchange = () => {
    cate = category.value;
    fetch('/admin/products/new' + cate).then(function (response) {
      response.json().then(function (data) {
        let optionHTML = '';
        console.log(data);
      });

    });
  };
});
