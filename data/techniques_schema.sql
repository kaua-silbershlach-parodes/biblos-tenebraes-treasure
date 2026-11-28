CREATE TABLE techniques (
    id             VARCHAR2(16) PRIMARY KEY,
    title          VARCHAR2(200),
    text           CLOB,
    e5_vector      VECTOR(384, FLOAT32),
    minilm_vector  VECTOR(384, FLOAT32)
);

CREATE TABLE book_chunks (
    id             NUMBER PRIMARY KEY,
    book           NUMBER,
    page           NUMBER,
    text           CLOB,
    e5_vector      VECTOR(384, FLOAT32),
    minilm_vector  VECTOR(384, FLOAT32)
);
