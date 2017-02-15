const gulp = require('gulp');
const sftp = require('gulp-sftp');

gulp.task('deploy', function () {
    return gulp.src('**/*')
        .pipe(sftp({
            host: 'b.ruub.eu',
            remotePath: "apps/thesis-backend/public",
            auth: 'main'
        }));
});

gulp.task('default', function () {
    return gulp.src('*')
        .pipe(sftp({
            host: 'b.ruub.eu',
            remotePath: "apps/thesis-backend/public",
            auth: 'main'
        }));
});