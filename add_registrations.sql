DELIMITER //

CREATE PROCEDURE generate_registrations()
BEGIN
    DECLARE s INT DEFAULT 1;
    DECLARE c1 INT;
    DECLARE c2 INT;
    DECLARE c3 INT;

    WHILE s <= 50 DO
        SET c1 = ((s - 1) MOD 12) + 1;
        SET c2 = ((s + 3) MOD 12) + 1;
        SET c3 = ((s + 7) MOD 12) + 1;

        INSERT INTO registrations (student_id, course_id, registration_date, status)
        VALUES
        (s, c1, '2026-06-27', 'Registered'),
        (s, c2, '2026-06-28', 'Registered'),
        (s, c3, '2026-06-29', 'Registered');

        SET s = s + 1;
    END WHILE;
END //

DELIMITER ;

CALL generate_registrations();

DROP PROCEDURE generate_registrations;
