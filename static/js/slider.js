function min_value(x)
{
	x=parseInt(x);
	if (check_if_too_high(x)===false){document.getElementById("slider").innerHTML=x;
	document.getElementById("slider_info_min").setAttribute("value",x);
	}
 console.log("1",document.getElementById("slider2"),"2",
		document.getElementById("slider_info_min"),"3",document.getElementById("slider"),"4",
		document.getElementById("slider_info_max"));
}


function max_value(x)
{
	x=parseInt(x);
	if (check_if_too_low(x)===false){document.getElementById("slider2").innerHTML=x;
	document.getElementById("slider_info_max").setAttribute("value",x);}
	console.log("1",document.getElementById("slider2"),"2",
		document.getElementById("slider_info_min"),"3",document.getElementById("slider"),"4",
		document.getElementById("slider_info_max"));
}

function check_if_too_high(x)
{
	var two = document.getElementById("slider_info_max");
	var max = two.getAttribute("value");
	max=parseInt(max);
	if (x>max) 
	{
		document.getElementById("slider").innerHTML=max;
		m = document.getElementById("slider_info_min");
		m.setAttribute("value",max);
		return true;
	}
	else
	{	
		return false;
	}
}

function check_if_too_low(x)
{
	var one = document.getElementById("slider_info_min");
	var min = one.getAttribute("value");
	min=parseInt(min);
	if (x<min) 
	{
		document.getElementById("slider2").innerHTML=min;
		m = document.getElementById("slider_info_max");
		m.setAttribute("value",min);
		return true;
	}
	else {
		
		return false;
	}
}

