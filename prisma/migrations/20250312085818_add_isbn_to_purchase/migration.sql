-- CreateTable
CREATE TABLE "user" (
    "user_line_id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "surname" TEXT NOT NULL,
    "email" TEXT NOT NULL,

    CONSTRAINT "user_pkey" PRIMARY KEY ("user_line_id")
);

-- CreateTable
CREATE TABLE "booklist" (
    "bibid" SERIAL NOT NULL,
    "title" TEXT NOT NULL,
    "author" TEXT NOT NULL,
    "table_of_content" TEXT,
    "subject" TEXT,

    CONSTRAINT "booklist_pkey" PRIMARY KEY ("bibid")
);

-- CreateTable
CREATE TABLE "userquery" (
    "query_id" TEXT NOT NULL,
    "user_line_id" TEXT NOT NULL,
    "user_query" TEXT NOT NULL,
    "response_success" TEXT,
    "response_purchase" TEXT,
    "time_stamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "userquery_pkey" PRIMARY KEY ("query_id")
);

-- CreateTable
CREATE TABLE "purchase" (
    "query_id" TEXT NOT NULL,
    "response_pick" TEXT NOT NULL,
    "isbn" TEXT NOT NULL,

    CONSTRAINT "purchase_pkey" PRIMARY KEY ("query_id")
);

-- CreateIndex
CREATE UNIQUE INDEX "user_email_key" ON "user"("email");

-- AddForeignKey
ALTER TABLE "userquery" ADD CONSTRAINT "userquery_user_line_id_fkey" FOREIGN KEY ("user_line_id") REFERENCES "user"("user_line_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "purchase" ADD CONSTRAINT "purchase_query_id_fkey" FOREIGN KEY ("query_id") REFERENCES "userquery"("query_id") ON DELETE CASCADE ON UPDATE CASCADE;
