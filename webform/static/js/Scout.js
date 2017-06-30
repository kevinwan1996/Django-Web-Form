function Scout(first_name, last_name, scout_id, gender, age, street, city, state, zip, phone, email, emergency_firstname, emergency_lastname, emergency_phone, affiliation, scout_username, scout_password) {
	this.first_name = first_name;
	this.last_name = last_name;
	this.scout_id = scout_id;
	this.gender = gender;
	this.age = age;
	this.street = street;
	this.city = city;
	this.state = state;
	this.zip = zip;
	this.phone = phone;
	this.email = email;
	this.emergency_firstname = emergency_firstname;
	this.emergency_lastname = emergency_lastname;
	this.emergency_phone = emergency_phone;
	this.affiliation = affiliation;
	this.scout_username = scout_username;
	this.scout_password = scout_password;

	this.setFirstName = function(newName){
		this.first_name = newName;
	}
	this.getFirstName = function(){
		return this.first_name;
	}
	this.setLastName = function(newName){
		this.last_name = newName;
	}
	this.getLastName = function(){
		return this.last_name;
	}
	this.getID = function(){
		return this.scout_id;
	}
	this.setGender = function(newGender){
		this.gender = newGender;
	}
	this.getGender = function(){
		return this.gender;
	}
	this.setAge = function(newAge){
		this.age = newAge;
	}
	this.getInstructor = function(){
		return this.age;
	}
	this.setStreet = function(newStreet){
		this.street = newStreet;
	}
	this.getStreet = function(){
		return this.street;
	}
	//TODO ADD MORE

	this.setPhone = function(newPhone){
		this.phone = newPhone;
	}
	this.getPhone = function(){
		return this.phone;
	}
	this.setEmail = function(newEmail){
		this.email = newEmail;
	}
	this.getEmail = function(){
		return this.email;
	}
	this.setAffiliation = function(newAffiliation){
		this.affiliation = newAffiliation;
	}
	this.getAffiliation = function(){
		return this.affiliation;
	}



	this.commitToDatabase = function(){
		//To be implemented
	}
}

function getAllScouts(callback) {
	/* call the php that has the php array which is json_encoded */
    console.log('Getting JSON');
    $.getJSON('getScouts.php', function(data) {
	   	console.log('loaded JSON');
	    var scouts = []; // create array here
	    $.each(data, function(index, scoutObject) {
	    	scouts.push(new Scout(scoutObject.first_name, 
		    		scoutObject.last_name, 
		    		scoutObject.scout_id, 
		    		scoutObject.gender, 
		    		scoutObject.age, 
		    		scoutObject.street, 
		    		scoutObject.city, 
		    		scoutObject.state, 
		    		scoutObject.zip, 
		    		scoutObject.phone, 
		    		scoutObject.email, 
		    		scoutObject.emergency_firstname, 
		    		scoutObject.emergency_lastname, 
		    		scoutObject.emergency_phone, 
		    		scoutObject.affiliation, 
		    		scoutObject.scout_username, 
		    		scoutObject.scout_password));
	    });
		callback.call(this,scouts);
    });
    console.log("After function")
}