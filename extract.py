import pypdf
def extract_text_from_pdf(pdf_path,output_path,start_marker, end_marker):


    print(f"{pdf_path} is opening....")
    reader = pypdf.PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(total_pages)

    extracted_segment = []
    is_extracting = False

    for page_num in range(total_pages):
       page = reader.pages[page_num]
       text = page.extract_text()

       if not text:
        continue

       text=text.strip()
       lower_text = text.lower()

       events=[]
       start_index = 0

       for marker in start_marker:
        index = lower_text.find(marker)
        while(index != -1):
            events.append((index, 'start', marker))
            index = lower_text.find(marker,index+1)
            
       for marker in end_marker:
        index = lower_text.find(marker)
        while(index != -1):
            events.append((index, 'end', marker))
            index = lower_text.find(marker,index+1)

       events.sort(key=lambda x: x[0])

       for index,event_type,marker in events:
            if event_type == 'start' and not is_extracting:
                print(f"Page {page_num + 1}: Found start marker '{marker}' at index {index}")
                is_extracting = True
                start_index = index

            elif event_type == 'end' and is_extracting:
                print(f"Page {page_num + 1}: Found end marker '{marker}' at index {index}")
                segment =text[start_index:index]
                extracted_segment.append(f"\n--- Section Page {page_num+1} ---\n{segment}\n")
                is_extracting = False

       if(is_extracting):
            segment = text[start_index:] 
            extracted_segment.append(f"\n--- Section Page {page_num+1} (cont.) ---\n{segment}\n")
            start_index = 0       
               
                
    print(f"Saving extracted sections to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(extracted_segment)
        
    print("Successfully completed extraction!")

pdf_path = r"C:\Users\amrit\Downloads\TCS_NQT_Previous_Year_Papers_with_Solutions_by_Placement_Lelo_1.pdf"
output_path = r"D:\text extractor\output.txt"
start_marker = ["reasoning ability","advanced reasoning"]
end_marker=["advanced coding","tcs nqt"]

extract_text_from_pdf(pdf_path, output_path,start_marker, end_marker)
