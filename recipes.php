<?php

require_once './vendor/autoload.php';

use sylouuu\MarmitonCrawler\Recipe\Recipe;

function get_links($url) {

	global $recipes;
	$input = @file_get_contents($url);
	$regexp = "<a\s[^>]*href=(\"??)([^\" >]*?)\\1[^>]*>(.*)<\/a>";
	preg_match_all("/$regexp/siU",$input,$matches);
	$base_url = parse_url($url,PHP_URL_HOST);

	$l = $matches[2];
	foreach ($l as $link) {

		if (strpos($link, "#")) {
			$link = substr($link,0,strpos($link,"#"));
		}
		if (substr($link,0,1) == ".") {
			$link = substr($link,1);
		}

		if (substr($link,0,7) == "http://") {
			$link = $link ;
		} else if (substr($link,0,8) == "https://") {
			$link = $link;
		} else if (substr($link,0,2) == "//") {
			$link = substr($link,2);
		} else if (substr($link,0,1) == "#") {
			$link = $url;
		} else if (substr($link,0,7) == "mailto:") {
			$link = "[".$link."]";
		} 

		if (substr($link,0,1) == "'") {
			$link = substr($link,1,strlen($link)-1);
		}
		if (substr($link,-1) == "'") {
			$link = substr($link,0,strlen($link)-1);
		}

		if (substr($link,0,1) == "/") {
			$link = $base_url.$link;
		}

		if (substr($link,0,7) != "http://" && substr($link,0,8) != "https://" && substr($link,0,1) != "[") {
			if (substr($url,0,8) == "https://") {
				$link = "https://".$link;
			} else {
				$link = "http://".$link;
			}
		}

		if (!in_array($link, $recipes) && preg_match('/recettes\/recette_/', $link)) {
			array_push($recipes, $link);
		}
	}

	return $recipes;

}

# ======
#  MAIN
# ======


$to_crawl = "http://www.marmiton.org/recettes/recette-hasard.aspx";
$recipes = array();

foreach (get_links($to_crawl) as $page) {
	$recipe = new Recipe($page);
	$recipe = $recipe -> getRecipe();
	print $recipe."\n";
	$file = fopen('sorties_02122016.txt', 'a');
	fwrite($file, $recipe."\n");
	fclose($file);
}

/*
$page = 'http://www.marmiton.org/recettes/recette_vacherin-aux-fraises-en-verrine_88208.aspx';
$recipe = new Recipe($page);
$recipe = $recipe -> getRecipe();	
print $recipe."\n";
*/

?>