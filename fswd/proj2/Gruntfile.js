module.exports = function(grunt) {
  grunt.initConfig({
    imagemin: {
      jpg: {
        options: { progressive: true },
        files: {
          'production/img/chess.jgp': 'production/img/chess-small.jpg',
          'production/img/hf-trading.jgp': 'production/img/hf-trading-small.jpg',
          'production/img/movie-studio.jgp': 'production/img/movie-studio-small.jpg'
        }
      }
    },
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
    cssmin: {
      target: {
        files: { 'production/css/style.min.css': 'css/style.css' }
      }
    },
    htmlmin: {
      options: { collapseWhitespace: true },
      target: {
        files: { 'production/index.html': 'index.html' }
      }
    },
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
    csslint: {
      strict: {
        src: ['css/style.css']
      }
    }
  });
	
  grunt.loadNpmTasks('grunt-contrib-imagemin');
  grunt.loadNpmTasks('grunt-responsive-images');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-htmlmin');
  grunt.loadNpmTasks('grunt-w3c-html-validation');
  grunt.loadNpmTasks('grunt-contrib-csslint');

  grunt.registerTask('imgopt', ['imagemin']);
  grunt.registerTask('sizeopt', ['responsive_images']);
  grunt.registerTask('cssopt', ['cssmin']);
  grunt.registerTask('htmlopt', ['htmlmin']);
  grunt.registerTask('valid', ['validation']);
  grunt.registerTask('css', ['csslint']);
  grunt.registerTask('default',
    [
      'validation',
      'csslint',
      'htmlmin',
      'cssmin',
      'responsive_images',
      'imagemin'
    ]
  );
};
