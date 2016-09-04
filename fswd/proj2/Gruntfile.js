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
	  },
    responsive_images: {
      ostask: {
	      options: {
	        engine: 'im',
	        concurrency: 3,
	        newFilesOnly: true
	      },
	      files: [{
	        expand: true,
	        src: ['img/**.{jpg,png}'],
	        dest: 'img/responsive'
	      }]
      }
    }
	});
	
	grunt.loadNpmTasks('grunt-contrib-imagemin');
	grunt.loadNpmTasks('grunt-responsive-images');
	grunt.registerTask('imgopt', ['imagemin']);
	grunt.registerTask('optsize', ['responsive_images']);
};
