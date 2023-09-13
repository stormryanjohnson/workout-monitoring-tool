
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'activities')
BEGIN
    CREATE TABLE activities (
        id INT PRIMARY KEY,
        [type] VARCHAR(255),
        distance DECIMAL(8, 2),
        moving_time INT,
        elapsed_time INT,
        total_elevation_gain DECIMAL(8, 2),
        start_date_local DATETIME,
        average_speed DECIMAL(8, 3),
        max_speed DECIMAL(8, 3),
        average_heartrate DECIMAL(8, 3),
        max_heartrate DECIMAL(8, 3),
        elev_high DECIMAL(8, 2),
        elev_low DECIMAL(8, 2),
        start_latitude DECIMAL(10, 8),
        start_longitude DECIMAL(11, 8),
        end_latitude DECIMAL(10, 8),
        end_longitude DECIMAL(11, 8)
    );

    BULK INSERT activities
    FROM '/Users/storm/Documents/GitHub/workout-monitoring-tool/df.csv'
    WITH (
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        FIRSTROW = 2
    );
END;


IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'segments')
BEGIN
    CREATE TABLE segments (
        id BIGINT PRIMARY KEY,
        name VARCHAR(255),
        activity_id BIGINT,
        elapsed_time INT,
        moving_time INT,
        start_date_local DATETIME,
        distance DECIMAL(8, 1),
        start_index INT,
        end_index INT,
        average_heartrate DECIMAL(8, 1),
        max_heartrate DECIMAL(8, 1)
    );

    -- Import data into the 'segments' table from CSV
    BULK INSERT segments
    FROM '/Users/storm/Documents/GitHub/workout-monitoring-tool/seg.csv'
    WITH (
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        FIRSTROW = 2
    );
END;


IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'segments_expanded')
BEGIN
    CREATE TABLE segments_expanded (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        activity_id BIGINT,
        activity_type VARCHAR(50),
        distance DECIMAL(8, 1),
        average_grade DECIMAL(4, 1),
        maximum_grade DECIMAL(4, 1),
        elevation_high DECIMAL(4, 1),
        elevation_low DECIMAL(4, 1),
        elevation_profile VARCHAR(255),
        climb_category INT,
        city VARCHAR(255),
        state VARCHAR(255),
        country VARCHAR(255),
        start_latitude DECIMAL(10, 6),
        start_longitude DECIMAL(10, 6),
        end_latitude DECIMAL(10, 6),
        end_longitude DECIMAL(10, 6)
    );

    BULK INSERT segments_expanded
    FROM '/Users/storm/Documents/GitHub/workout-monitoring-tool/single_seg.csv'
    WITH (
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        FIRSTROW = 2
    );
END;
