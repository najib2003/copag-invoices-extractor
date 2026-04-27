Local offline batch invoice extraction for company PDFs and image invoices.

The MVP reads a PDF or image, treats one page as one invoice, runs PaddleOCR on the original page first, optionally tries OpenCV fallback variants when quality is weak, extracts only selected business fields, and exports one Excel row per invoice.

