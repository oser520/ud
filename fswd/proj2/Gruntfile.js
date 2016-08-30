module.exports = function(grunt) {
	grunt.initConfig({
	  imagemin: {
	    png: {
	      files: [
	        {
	          expand: true,
	          cwd: 'img/',
	          src: ['**/*.png'],
	          dest: './img/compressed/',
	          ext: '.png'
	        }
	      ]
	    },
	    jpg: {
	      options: { progressive: true },
	      files: [
	        {
	          expand: true,
	          cwd: 'img/',
	          src: ['**/*.jpg'],
	          dest: './img/compressed',
	          ext: '.jpg'
	        }
	      ]
	    }
	  }
	});
	
	grunt.loadNpmTasks('grunt-contrib-imagemin');
	grunt.registerTask('imgopt', ['imagemin']);
};
