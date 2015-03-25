/*----------------------------------------------------------------------------*/
/* initalization.sql                                                          */
/* -----------------                                                          */
/* Script which generates the initial content necessary to render in the app. */
/*                                                                            */
/*----------------------------------------------------------------------------*/

/*--------------------*/
/* at_course_previews */
/*--------------------*/
INSERT INTO at_course_previews (id, image_filename, title, sub_title, category, description, summary)
VALUES
(1, 'roundicons.png', 'Comics Book Course', 'The definitive course on comics and western drawings!', 'Liberal Arts', '<p>\nUse this area to describe your project. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Est blanditiis dolorem culpa incidunt minus dignissimos deserunt repellat aperiam quasi sunt officia expedita beatae cupiditate, maiores repudiandae, nostrum, reiciendis facere nemo!\n</p>', '');

/*------------------------------*/
/* at_landpage_course_previews  */
/*------------------------------*/
INSERT INTO at_landpage_course_previews (id, image_filename, title, category)
VALUES
(1, 'roundicons-preview.png', 'Comics Book Course', 'Liberal Arts');


/*---------------------------*/
/* at_landpage_team_members  */
/*---------------------------*/
INSERT INTO at_landpage_team_members (id, full_name, role, twitter_url, facebook_url, image_filename, linkedin_url, email)
VALUES
(1, 'Bartlomiej Mika', 'Lead Developer', 'https://twitter.com/BartlomiejMika', 'https://www.facebook.com/bartlomiej.mika', 'bartlomiejmika.png', 'https://www.linkedin.com/pub/bartlomiej-mika/3b/568/a9a', '');

INSERT INTO at_landpage_team_members (id, full_name, role, twitter_url, facebook_url, image_filename, linkedin_url, email)
VALUES
(2, 'Michael Murray', 'Lead Designer', '', '', 'michaelmurray.png', '', '');

INSERT INTO at_landpage_team_members (id, full_name, role, twitter_url, facebook_url, image_filename, linkedin_url, email)
VALUES
(3, 'Sebastion Rydzewski', 'Developer', 'https://twitter.com/@srydzewski_AT', '', 'sebastionrydzewski.png', 'http://ca.linkedin.com/pub/sebastian-rydzewski/5b/108/160', 'srydzewski.AT@gmail.com');

/*-----------------------*/
/* at_landpage_partners  */
/*-----------------------*/
INSERT INTO at_landpage_partners (id, image_filename, title, url)
VALUES
(1, 'duplexsoft.png', 'Duplexsoft', 'www.duplexsoft.com');

INSERT INTO at_landpage_partners (id, image_filename, title, url)
VALUES
(2, 'eurasiasoft.png', 'Eurasiasoft', 'www.eurasiasoft.com');
