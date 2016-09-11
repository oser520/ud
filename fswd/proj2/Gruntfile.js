var fs = require('fs');

module.exports = function(grunt) {
  grunt.initConfig({
    /* Check HTML does not contain any errors */
    validation: {
      options: {
        doctype: 'HTML5',
        stoponerror: true,
        relaxerror: ['Empty heading.']
      },
      files: {
        src: ['index.html']
      }
    },
    /* Check CSS does not contain any errors */
    csslint: {
      strict: {
        src: ['css/style.css']
      }
    },
    /* Remove whitespace from the HTML */
    htmlmin: {
      options: { collapseWhitespace: true },
      target: {
        files: { 'production/index.html': 'index.html' }
      }
    },
    /* Remove whitespace from the CSS */
    cssmin: {
      target: {
        files: { 'production/css/style.min.css': 'css/style.css' }
      }
    },
    /* Make the images smaller */
    responsive_images: {
      ostask: {
        options: {
          engine: 'im',
          concurrency: 3,
          newFilesOnly: true,
          sizes: [
            {name: 'small', width: 320}
          ]
        },
        files: [{
          expand: true,
          cwd: '.',
          src: ['img/**.{jpg,png}'],
          dest: 'production/'
        }]
      }
    },
    /* Compress the images */
    imagemin: {
      jpg: {
        options: { progressive: true },
        files: {
          'production/img/chess.jgp': 'production/img/chess-small.jpg',
          'production/img/hf-trading.jgp': 'production/img/hf-trading-small.jpg',
          'production/img/movie-studio.jgp': 'production/img/movie-studio-small.jpg'
        }
      }
    }
  });
	
  grunt.loadNpmTasks('grunt-contrib-imagemin');
  grunt.loadNpmTasks('grunt-responsive-images');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-htmlmin');
  grunt.loadNpmTasks('grunt-w3c-html-validation');
  grunt.loadNpmTasks('grunt-contrib-csslint');

  /* Note that some of these have dependencies, and thus will not work unless
   * their dependencies are executed first
   */
  grunt.registerTask('valid', ['validation']);
  grunt.registerTask('css', ['csslint']);
  grunt.registerTask('htmlopt', ['htmlmin']);
  grunt.registerTask('cssopt', ['cssmin']);
  grunt.registerTask('sizeopt', ['responsive_images']);
  grunt.registerTask('imgopt', ['imagemin']);
  grunt.registerTask('clean', 'Remove temporary files', function() {
    fs.unlink('production/img/chess-small.jpg');
    fs.unlink('production/img/hf-trading-small.jpg');
    fs.unlink('production/img/movie-studio-small.jpg');
  });
  grunt.registerTask('default',
    [
      'validation',
      'csslint',
      'htmlmin',
      'cssmin',
      'responsive_images',
      'imagemin',
      'clean'
    ]
  );
};
