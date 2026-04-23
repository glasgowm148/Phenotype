function CustomTooltip(tooltipId, width){
	var tooltipId = tooltipId;
	$("body").append("<div class='tooltip' id='"+tooltipId+"'></div>");
	
	if(width){
		$("#"+tooltipId).css("width", width);
	}
	
	hideTooltip();
	


	function Listcategories(content){
		$
	}

	function showTooltip(content, x, y){
		$("#"+tooltipId).html(content);
		$("#"+tooltipId).show();
		
		updatePosition(x,y);
	}
	
	function hideTooltip(){
		$("#"+tooltipId).hide();
	}
	
	function updatePosition(x,y){
		var ttid = "#"+tooltipId;
		var xOffset = 50;
		var yOffset = 25;
		
		 var ttw = $(ttid).width();
		 var tth = $(ttid).height();
		 var wscrY = $(window).scrollTop();
		 var wscrX = $(window).scrollLeft();
		// var curX = (document.all) ? element.clientX + wscrX : element.pageX;
		// var curY = (document.all) ? element.clientY + wscrY : element.pageY;
	       var curX = x;
		   var curY = y;
/*		 var ttleft = ((curX - wscrX + xOffset*2 + ttw) > $(window).width()) ? curX - ttw - xOffset*2 : curX + xOffset;
		 if (ttleft < wscrX + xOffset){
		 	ttleft = wscrX + xOffset;
		 } 
		 var tttop = ((curY - wscrY + yOffset*2 + tth) > $(window).height()) ? curY - tth - yOffset*2 : curY + yOffset;
		 if (tttop < wscrY + yOffset){
		 	tttop = curY + yOffset;
		 } */
		 var ttleft = curX - 80;
		 var tttop = curY - 180;
		 $(ttid).css('top', tttop + 'px').css('left', ttleft + 'px');
	}
	
	return {
		showTooltip: showTooltip,
		hideTooltip: hideTooltip,
		updatePosition: updatePosition
	}
}
