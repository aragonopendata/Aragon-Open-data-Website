angular.module('aosd.filters', [])

  /* Twitter entities filter */
  .filter('removeTwitterChar', function() {
  	return function(input) {
  		return (input[0] == '@' || input[0] == '#') ? input.substring(1, input.length) : input;
  	};
  })

  .filter('capitalize', function() {
  	return function(input) {
  		return input.charAt(0).toUpperCase() + input.slice(1);
  	}
  })

  .filter('titleCase', function(helpers) {
    return function(input) {
      return helpers.titleCase(input);
    }
  })

  .filter('snakeCase', function() {
    return function(input) {
      var output = [];
      for (i=0; i<input.length; i++) {
        if (input[i] == '_' && i<input.length -1) {
          output.push(' ');
          output.push(input[i+1].toUpperCase());
          i++;
        } else {
          output.push(input[i]);
        }
      }
      return output.join('');
    }
  })

  .filter('trim', function() {
    return function(input) {
      return (input !== null) ? input.trim() : null;
    }
  });