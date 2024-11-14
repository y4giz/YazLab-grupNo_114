var restAPIAddress = "127.0.0.1";
async function checkLoggedinUser()
{
	if(localStorage.getItem('Authorization'))
	{	
		var authHeader = localStorage.getItem('Authorization');
		var username = parseJwt(authHeader).identity;
		document.getElementById("session-control").innerHTML = "<a href=\"profile.html\">Welcome, "+username+"</a>";
	}
	else
	{
		document.getElementById("session-control").innerHTML = "<a href=\"login.html\" class=\"nav-item nav-link\">Login</a>"+
																"<a href=\"register.html\" class=\"nav-item nav-link\">Register</a>";
	}	
}
async function checkAuthorizationHeader()
{
	if(localStorage.getItem('Authorization'))
	{
		return true;
	}
	else
	{
		window.location.href = 'login.html';
		return false;
	}
}

async function getCategories()
{
	fetch('http://'+restAPIAddress+':5000/categories')
    .then(response => response.json())
    .then(data => {
        var categories = data.categories;
        var categoriesHTML = "";
        for (var i = 0; i < categories.length; i++) 
		{
            categoriesHTML += "<a href=\"\" class=\"nav-item nav-link\">" + categories[i].category_name + "</a>";
        }
        document.getElementById("category-menu").innerHTML = categoriesHTML;
    })
    .catch(error => {
        console.error(error);
    });
}

async function getTrandyProducts()
{
	fetch('http://'+restAPIAddress+':5000/products/trandy')
    .then(response => response.json())
    .then(data => {
        var products = data.trandy_products;
        var productsHTML = "";
        for (var i = 0; i < products.length; i++) 
		{
            productsHTML += "<div class=\"col-lg-3 col-md-6 col-sm-12 pb-1\">"+
										"<div class=\"card product-item border-0 mb-4\">"+
											"<div class=\"card-header product-img position-relative overflow-hidden bg-transparent border p-0\">"+
												"<img class=\"img-fluid w-100\" src=\"img/rings/"+products[i].product_image+"\" alt=\""+products[i].product_image+"\">"+
											"</div>"+
											"<div class=\"card-body border-left border-right text-center p-0 pt-4 pb-3\">"+
												"<h6 class=\"text-truncate mb-3\">"+products[i].product_name+"</h6>"+
												"<div class=\"d-flex justify-content-center\">"+
													"<h6>$"+products[i].product_price+"</h6>"+
												"</div>"+
											"</div>"+
											"<div class=\"card-footer d-flex justify-content-between bg-light border\">"+
												"<a href=\"\" class=\"btn btn-sm text-dark p-0\"><i class=\"fas fa-eye text-primary mr-1\"></i>View Detail</a>"+
												"<a href=\"\" class=\"btn btn-sm text-dark p-0\"><i class=\"fas fa-shopping-cart text-primary mr-1\"></i>Add To Cart</a>"+
											"</div>"+
										"</div>"+
									"</div>";
        }
        document.getElementById("trandy-products").innerHTML = productsHTML;
    })
    .catch(error => {
        console.error(error);
    });
	
}

async function getAllProducts()
{
	fetch('http://'+restAPIAddress+':5000/products/all')
    .then(response => response.json())
    .then(data => {
        var products = data.products;
        var productsHTML = "";
        for (var i = 0; i < products.length; i++) 
		{
            productsHTML += "<div class=\"col-lg-3 col-md-6 col-sm-12 pb-1\">"+
										"<div class=\"card product-item border-0 mb-4\">"+
											"<div class=\"card-header product-img position-relative overflow-hidden bg-transparent border p-0\">"+
												"<img class=\"img-fluid w-100\" src=\"img/rings/"+products[i].product_image+"\" alt=\""+products[i].product_image+"\">"+
											"</div>"+
											"<div class=\"card-body border-left border-right text-center p-0 pt-4 pb-3\">"+
												"<h6 class=\"text-truncate mb-3\">"+products[i].product_name+"</h6>"+
												"<div class=\"d-flex justify-content-center\">"+
													"<h6>$"+products[i].product_price+"</h6>"+
												"</div>"+
											"</div>"+
											"<div class=\"card-footer d-flex justify-content-between bg-light border\">"+
												"<a href=\"./detail.html?product_id="+products[i].product_id+"\" class=\"btn btn-sm text-dark p-0\"><i class=\"fas fa-eye text-primary mr-1\"></i>View Detail</a>"+
												"<a href=\"\" class=\"btn btn-sm text-dark p-0\"><i class=\"fas fa-shopping-cart text-primary mr-1\"></i>Add To Cart</a>"+
											"</div>"+
										"</div>"+
									"</div>";
        }
        document.getElementById("all-products").innerHTML = productsHTML;
    })
    .catch(error => {
        console.error(error);
    });
	
}

async function getProductDetail()
{
	
	let currentUrl = window.location.href;
	let params = new URLSearchParams(currentUrl.split('?')[1]);
	let product_id = params.get('product_id');
	fetch('http://'+restAPIAddress+':5000/product/'+product_id)
    .then(response => response.json())
    .then(data => {
        var product = data;
        var productHTML = "";
		productHTML += "<div class=\"col-lg-5 pb-5\">"+
							"<div id=\"product-carousel\" class=\"carousel slide\" data-ride=\"carousel\">"+
								"<div class=\"carousel-inner border\">"+
									"<div class=\"carousel-item active\">"+
										"<img class=\"w-100 h-100\" id=\"image_path\" src=\"img/rings/"+product.product_image+"\" alt=\""+product.product_image+"\">"+
									"</div>"+
								"</div>"+
								"<a class=\"carousel-control-prev\" href=\"#product-carousel\" data-slide=\"prev\">"+
									"<i class=\"fa fa-2x fa-angle-left text-dark\"></i>"+
								"</a>"+
								"<a class=\"carousel-control-next\" href=\"#product-carousel\" data-slide=\"next\">"+
									"<i class=\"fa fa-2x fa-angle-right text-dark\"></i>"+
								"</a>"+
							"</div>"+
						"</div>"+

						"<div class=\"col-lg-7 pb-5\">"+
							"<h3 class=\"font-weight-semi-bold\">"+product.product_name+"</h3>"+
							"<div class=\"d-flex mb-3\">"+
								"<div class=\"text-primary mr-2\">"+
									"<small class=\"fas fa-star\"></small>"+
									"<small class=\"fas fa-star\"></small>"+
									"<small class=\"fas fa-star\"></small>"+
									"<small class=\"fas fa-star-half-alt\"></small>"+
									"<small class=\"far fa-star\"></small>"+
								"</div>"+
								"<small class=\"pt-1\">(50 Reviews)</small>"+
							"</div>"+
							"<h3 class=\"font-weight-semi-bold mb-4\">$"+product.product_price+"</h3>"+
							"<p class=\"mb-4\">"+product.product_description+"</p>"+
							"<div class=\"d-flex align-items-center mb-4 pt-2\">"+
								"<div class=\"input-group quantity mr-3\" style=\"width: 130px;\">"+
									"<input type=\"text\" class=\"form-control bg-secondary text-center\" value=\"1\" id=\"product-quantity\">"+
								"</div>"+
								"<button class=\"btn btn-primary px-3\" onclick=\"addBasket()\"><i class=\"fa fa-shopping-cart mr-1\"></i> Add To Basket</button>"+
							"</div>"+
							"<br>"+
							"<p id=\"adding-result\"></p>"+
							"<br>"+
							"<div class=\"d-flex pt-2\">"+
								"<p class=\"text-dark font-weight-medium mb-0 mr-2\">Share on:</p>"+
								"<div class=\"d-inline-flex\">"+
									"<a class=\"text-dark px-2\" href=\"\">"+
										"<i class=\"fab fa-facebook-f\"></i>"+
									"</a>"+
									"<a class=\"text-dark px-2\" href=\"\">"+
										"<i class=\"fab fa-twitter\"></i>"+
									"</a>"+
									"<a class=\"text-dark px-2\" href=\"\">"+
										"<i class=\"fab fa-linkedin-in\"></i>"+
									"</a>"+
									"<a class=\"text-dark px-2\" href=\"\">"+
										"<i class=\"fab fa-pinterest\"></i>"+
									"</a>"+
								"</div>"+
							"</div>"+
						"</div>";
        
        document.getElementById("product-detail").innerHTML = productHTML;
		document.getElementById("product_long_description").innerHTML = product.product_description;
    })
    .catch(error => {
        console.error(error);
    });
	
}

async function contact()
{
	fetch('http://'+restAPIAddress+':5000/contact', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
		subject: document.getElementById("subject").value,
		message: document.getElementById("message").value
    })
})
.then(response => response.json())
.then(data => {
        var message = data;
        document.getElementById("message-response").innerHTML = data.message;
    })
	.catch(error => {
        console.error(error);
    });
}

async function register()
{
	fetch('http://'+restAPIAddress+':5000/register', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        username: document.getElementById("username").value,
        email: document.getElementById("email").value,
		firstname: document.getElementById("firstname").value,
		lastname: document.getElementById("lastname").value,
		pass: document.getElementById("pass").value,
		pass2: document.getElementById("pass2").value
    })
})
.then(response => response.json())
.then(data => {
        var message = data;
        document.getElementById("registration-result").innerHTML = data.message;
    })
	.catch(error => {
        console.error(error);
    });
}

async function login()
{
	fetch('http://'+restAPIAddress+':5000/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        username: document.getElementById("username").value,
		pass: document.getElementById("pass").value
    })
})
.then(response => response.json())
.then(data => {
		if(data.token)
		{
			var token = data.token;
			localStorage.setItem('Authorization', token);
			if(localStorage.getItem('Authorization'))
			{
				window.location.href = 'profile.html';
			}
			else
			{
				
			}
		}
		else
		{
			var message = data;
			document.getElementById("login-result").innerHTML = data.message;
		}
    })
	.catch(error => {
        console.error(error);
    });
}

function logout()
{
	window.localStorage.removeItem('Authorization');
	window.location.href = 'index.html';
}

function getProfile()
{	
	var authHeader = localStorage.getItem('Authorization');
	fetch('http://'+restAPIAddress+':5000/profile/info', {headers: { 'Authorization': authHeader }})
	.then(response => response.json())
	.then(data => {
		var userInfo = data;
		document.getElementById("username").value = userInfo.username;
		document.getElementById("email").value = userInfo.email;
		document.getElementById("firstname").value = userInfo.firstname;
		document.getElementById("lastname").value = userInfo.lastname;
	})
	.catch(error => {
		console.error(error);
	});
}

function getWallet()
{	
	var authHeader = localStorage.getItem('Authorization');
	fetch('http://'+restAPIAddress+':5000/profile/wallet', {headers: { 'Authorization': authHeader }})
	.then(response => response.json())
	.then(data => {
		var walletInfo = data;
		document.getElementById("my-balance").innerHTML = 'My Balance: $' + walletInfo.balance;
	})
	.catch(error => {
		console.error(error);
	});
}

function deposit()
{
	var authHeader = localStorage.getItem('Authorization');
	fetch('http://'+restAPIAddress+':5000/profile/deposit', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
		'Authorization': authHeader
    },
    body: JSON.stringify({
        deposit: document.getElementById("deposit-value").value,
        cardnumber: document.getElementById("card-number").value,
		date: document.getElementById("date").value,
		cvc: document.getElementById("cvc").value
    })
})
.then(response => response.json())
.then(data => {
        var message = data;
        document.getElementById("deposit-result").innerHTML = data.message;
    })
	.catch(error => {
        console.error(error);
    });
}


async function getProductsInBasket()
{
	var authHeader = localStorage.getItem('Authorization');
	fetch('http://'+restAPIAddress+':5000/basket', {headers: { 'Authorization': authHeader }})
    .then(response => response.json())
    .then(data => {
        var basket = data.products_in_basket;
        var basketHTML = "";
		var total = 0;
		if(basket.length > 0)
		{
			for (var i = 0; i < basket.length; i++) 
			{
				basketHTML +=   "<tr>"+
									"<td><img src=\"img/rings/"+basket[i].product_image+"\" style=\"width:20%; height:20%;\"></td>"+
									"<td>"+
										"<h6>"+basket[i].product_name+"</h6>"+
										"<p>Quantity: "+basket[i].product_quantity+"</p>"+
										"<p>Total: $"+basket[i].total+"</p>"+
										"<br>"+
									"</td>"+
								"</tr>";
				total += parseFloat(basket[i].total);
			}
			document.getElementById("products-in-basket").innerHTML = basketHTML;
		}
		document.getElementById("basket-total").innerHTML = String(total);
    })
    .catch(error => {
        console.error(error);
    });
	
}

function clearBasket()
{	
	var authHeader = localStorage.getItem('Authorization');
	fetch('http://'+restAPIAddress+':5000/basket/clear', {headers: { 'Authorization': authHeader }})
	.then(response => response.json())
	.then(data => {
		var walletInfo = data;
		location.reload();
	})
	.catch(error => {
		console.error(error);
	});
}

function addBasket()
{
	if(checkAuthorizationHeader())
	{
		const urlParams = new URLSearchParams(window.location.search);
		const paramValue = urlParams.get('product_id');
		var authHeader = localStorage.getItem('Authorization');
		fetch('http://'+restAPIAddress+':5000/basket', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'Authorization': authHeader
		},
		body: JSON.stringify({
			product_id: paramValue,
			quantity: document.getElementById("product-quantity").value,
			image_path: "http://localhost:5000/"+document.getElementById('image_path').getAttribute('src')
		})
		})
		.then(response => response.json())
		.then(data => {
				var message = data;
				document.getElementById("adding-result").innerHTML = message.message;
			})
			.catch(error => {
				console.error(error);
			});
	}
	else
	{
		document.getElementById("adding-result").innerHTML = "You must login.";
	}
}

function buy()
{
	var authHeader = localStorage.getItem('Authorization');
	fetch('http://'+restAPIAddress+':5000/buy', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
		'Authorization': authHeader
    },
    body: JSON.stringify({
        total: parseFloat(document.getElementById("basket-total").innerHTML)
    })
})
.then(response => response.json())
.then(data => {
        var message = data;
        document.getElementById("order-result").innerHTML = data.message;
    })
	.catch(error => {
        console.error(error);
    });
}

function getOrders()
{
	var authHeader = localStorage.getItem('Authorization');
	fetch('http://'+restAPIAddress+':5000/orders', {headers: { 'Authorization': authHeader }})
	.then(response => response.json())
	.then(data => {
		var orders = data.my_orders;
		var ordersHTML = "";
		for (var i = 0; i < orders.length; i++) 
		{
            ordersHTML += "<div class=\"align-items-center border mb-4\" style=\"padding: 30px;\">"+
								"<p>"+orders[i].order_date+"</p>"+
								"<h3 class=\"fa fa-check text-primary m-0 mr-3\"> <a href=\"order_detail.html?order_id="+orders[i].order_id+"\">Order No: "+orders[i].order_id+"</a></h3>"+
								
								"<h5 class=\"font-weight-semi-bold m-0\"><BR>Order Total: $"+orders[i].order_total+"</h5>";
								for(var j = 0; j < orders[i].order_detail.length; j++)
								{
									ordersHTML += "<p>"+orders[i].order_detail[j].quantity+" "+orders[i].order_detail[j].product_name+" $"+orders[i].order_detail[j].total+"</p>";
								}
								
			ordersHTML += "</div>";
        }
        document.getElementById("my-orders").innerHTML = ordersHTML;
	})
	.catch(error => {
		console.error(error);
	});
}

function getOrderDetail()
{
	let currentUrl = window.location.href;
	let params = new URLSearchParams(currentUrl.split('?')[1]);
	let order_id = params.get('order_id');
	var authHeader = localStorage.getItem('Authorization');
	fetch('http://'+restAPIAddress+':5000/order/'+order_id, {headers: { 'Authorization': authHeader }})
    .then(response => response.json())
    .then(data => {
        var order = data.order;
        var orderHTML = "";
		var total = 0;
		if(order.length > 0)
		{
			if(order[0].order_detail.length > 0)
			{
				for (var i = 0; i < order[0].order_detail.length; i++) 
				{
					orderHTML +=   "<tr>"+
										"<td>"+
											"<div class=\"align-items-center border mb-4\" style=\"padding: 30px;\">"+
												"<h6>"+order[0].order_detail[i].product_name+"</h6>"+
												"<p>Quantity: "+order[0].order_detail[i].quantity+"</p>"+
												"<p>Total: $"+order[0].order_detail[i].total+"</p>"+
												"<br>"+
											"</div>"+
										"</td>"+
									"</tr>";
					total += parseFloat(order[0].order_detail[i].total);
				}
				document.getElementById("order-detail").innerHTML = orderHTML;
			}
		}
		document.getElementById("order-total").innerHTML = String(total)+" &nbsp;&nbsp;&nbsp;&nbsp; "+order[0].order_date+"&nbsp;&nbsp;&nbsp;&nbsp;  <h5 class=\"fa fa-user\ text-primary m-0 mr-3\"> "+order[0].orderer+"</h5>";
    })
    .catch(error => {
        console.error(error);
    });
	
}

function setAddress()
{
	var authHeader = localStorage.getItem('Authorization');
	var username = parseJwt(authHeader).identity;

	fetch('http://'+restAPIAddress+':5000/address/'+username, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
		'Authorization': authHeader
    },
    body: JSON.stringify({
        address_header: document.getElementById("header").value,
        address_content: document.getElementById("address").value
    })
	})
	.then(response => response.json())
	.then(data => {
			var message = data;
			document.getElementById("address-result").innerHTML = message.message;
		})
		.catch(error => {
			console.error(error);
		});
}


function getAddress()
{	
	var authHeader = localStorage.getItem('Authorization');
	var username = parseJwt(authHeader).identity;
	var authHeader = localStorage.getItem('Authorization');
	fetch('http://'+restAPIAddress+':5000/address/'+username, {headers: { 'Authorization': authHeader }})
	.then(response => response.json())
	.then(data => {
		var userAddress = data;
		document.getElementById("header").value = userAddress.address_header;
		document.getElementById("address").value = userAddress.address;
	})
	.catch(error => {
		console.error(error);
	});
}

function parseJwt (token) 
{
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

function subscribe()
{
		fetch('http://'+restAPIAddress+':5000/subscribe', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			name: document.getElementById("subscriber-name").value,
			email: document.getElementById("subscriber-email").value
		})
		})
		.then(response => response.json())
		.then(data => {
				var message = data;
				document.getElementById("subscribe-result").innerHTML = message.message;
			})
			.catch(error => {
				console.error(error);
			});
}

function subscribe2()
{
		fetch('http://'+restAPIAddress+':5000/subscribe', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			name: document.getElementById("subscriber-name").value,
			email: document.getElementById("subscriber-email2").value
		})
		})
		.then(response => response.json())
		.then(data => {
				var message = data;
				document.getElementById("subscribe-result2").innerHTML = message.message;
			})
			.catch(error => {
				console.error(error);
			});
}

function search()
{	
	var searchInput = document.getElementById("search-box").value;
	fetch('http://'+restAPIAddress+':5000/search/'+searchInput)
	.then(response => response.json())
	.then(data => {
		if(data.products)
		{
			var products = data.products;
			var productsHTML = "";
			for (var i = 0; i < products.length; i++) 
			{
				productsHTML += "<div class=\"col-lg-3 col-md-6 col-sm-12 pb-1\">"+
											"<div class=\"card product-item border-0 mb-4\">"+
												"<div class=\"card-header product-img position-relative overflow-hidden bg-transparent border p-0\">"+
													"<img class=\"img-fluid w-100\" src=\"img/rings/"+products[i].product_image+"\" alt=\""+products[i].product_image+"\">"+
												"</div>"+
												"<div class=\"card-body border-left border-right text-center p-0 pt-4 pb-3\">"+
													"<h6 class=\"text-truncate mb-3\">"+products[i].product_name+"</h6>"+
													"<div class=\"d-flex justify-content-center\">"+
														"<h6>$"+products[i].product_price+"</h6>"+
													"</div>"+
												"</div>"+
												"<div class=\"card-footer d-flex justify-content-between bg-light border\">"+
													"<a href=\"./detail.html?product_id="+products[i].product_id+"\" class=\"btn btn-sm text-dark p-0\"><i class=\"fas fa-eye text-primary mr-1\"></i>View Detail</a>"+
													"<a href=\"\" class=\"btn btn-sm text-dark p-0\"><i class=\"fas fa-shopping-cart text-primary mr-1\"></i>Add To Cart</a>"+
												"</div>"+
											"</div>"+
										"</div>";
			}
			document.getElementById("all-products").innerHTML = productsHTML;
		}
		else
		{
			document.getElementById("all-products").innerHTML = data.message;
		}
        
    })
	.catch(error => {
		console.error(error);
	});
}

async function updateUserInfo()
{
	var authHeader = localStorage.getItem('Authorization');
	var username = parseJwt(authHeader).identity;

	fetch('http://'+restAPIAddress+':5000/profile/info', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
		'Authorization': authHeader
    },
    body: JSON.stringify({
        email: document.getElementById("email").value,
        firstname: document.getElementById("firstname").value,
		lastname: document.getElementById("lastname").value,
		pass: document.getElementById("pass").value,
		pass2: document.getElementById("pass2").value,
    })
	})
	.then(response => response.json())
	.then(data => {
			var message = data;
			document.getElementById("updateinfo-result").innerHTML = message.message;
		})
		.catch(error => {
			console.error(error);
		});
}

async function passwordReset()
{
	var username = document.getElementById("username").value;
	fetch('http://'+restAPIAddress+':5000/forgotPassword/'+username)
	.then(response => response.json())
	.then(data => {
		if(data.reset_url)
		{
			document.getElementById("passreset-result").innerHTML = 'Password reset link has been sent to your email address';
		}
		else
		{
			document.getElementById("passreset-result").innerHTML = 'A problem was encountered';
		}
	})
	.catch(error => {
		console.error(error);
	});
}

async function changePassword()
{
	let currentUrl = window.location.href;
	let params = new URLSearchParams(currentUrl.split('?')[1]);
	let token = params.get('token');
	fetch('http://'+restAPIAddress+':5000/resetPassword/'+token, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        pass: document.getElementById("password").value,
        pass2: document.getElementById("password-repeat").value
    })
	})
	.then(response => response.json())
	.then(data => {
			var message = data;
			document.getElementById("passreset-result").innerHTML = message.message;
		})
		.catch(error => {
			console.error(error);
		});
}

var JWT_secret = 'Ring1234'; // this can be old.