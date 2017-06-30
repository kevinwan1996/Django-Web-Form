function Course(courseName, courseDescription, id) {
    this.courseName = courseName;
    this.courseDescription = courseDescription;
    this.id = id;

	this.setCourseName = function(newName){
		this.courseName = newName;
	}
	this.getCourseName = function(){
		return this.courseName;
	}
	this.setCourseDescription = function(newDescription){
		this.courseDescription = newDescription;
	}
	this.getCourseDescription = function(){
		return this.courseDescription;
	}
	this.getID = function(){
		return this.id;
	}
	this.setInstructor = function(newInstructor){
		this.instructor = newInstructor;
	}
	this.getInstructor = function(){
		return this.instructor;
	}
	this.setTime = function(newTime){
		this.time = newTime;
	}
	this.getTime = function(){
		return this.time;
	}

	this.commitToDatabase = function(){
		//To be implemented
	}
}

function getAllCourses(callback) {
  var courses = {{ all_courses|jsonify }}; // create array here
  // {% if all_courses %}
  //   console.log("GOOD!!!");
  //   {% for course in all_courses %}
  //     courses.push(new Course({{course.class_name}}, {{course.class_description}}, {{course.class_id}}));
  //   {% endfor %}
  // {% endif %}
	callback.call(this,courses);
}

function decodeJson(){
    console.log("INSIDE OF FUNCTION");


}
