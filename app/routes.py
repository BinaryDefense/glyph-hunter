from app import app
from flask import request, jsonify
from collections import Counter
from difflib import SequenceMatcher
import pytesseract
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

@app.route("/check", methods=["GET"])
def checkhomoglyphs():
    values = request.values
    if 'name' in values:
        name  = values['name']
    else:
        return('{"error":"must supply name value"}')
    if 'other_names' in values:
        other_names = values['other_names']
    else:
        other_names = None

    output = {'results':[]}

    if name:
        # check number of characters that are non-ascii
        non_ascii_chars_in_name = [c for c in name if ord(c) > 122]
        
        fontsize=13
        fontfullpath="./unifont-13.0.06.ttf"

        font = ImageFont.truetype(fontfullpath, fontsize)
        fgcolor = "#000000" # black
        bgcolor = "#FFFFFF" # white
        leftpadding = 5
        rightpadding = 5

        dimensions = font.getsize(name)
        width = dimensions[0] + leftpadding + rightpadding
        line_height = dimensions[1]
        img_height = line_height ##* (len(lines) + 1)

        img = Image.new("RGBA", (width, img_height), bgcolor)
        draw = ImageDraw.Draw(img) # fill with white
        draw.text((leftpadding, 0), name, fgcolor, font=font)

        ocr_text = pytesseract.image_to_string(img)
        ocr_text = ocr_text.replace("\n\u000c", "")
        ocr_text = ocr_text.strip()
        while ocr_text.endswith("."):
            ocr_text = ocr_text[:-1] # trim trailing periods
        # prepare single result
        result = {'new_name':name, 
                  'ocr_of_new_name':ocr_text, 
                  'ocr_similarity_to_new_name':similar(name, ocr_text), 
                  'name_is_as_it_seems':(name==ocr_text), 
                  'num_non_ascii_characters':len(non_ascii_chars_in_name), 
                  'non_ascii_characters':str(non_ascii_chars_in_name)}
        if other_names:
            other_names = other_names.split("||")
            for other_name in other_names:
                homoglyph_result = result.copy()
                homoglyph_result['homoglyph_score'] = similar(other_name, ocr_text)
                homoglyph_result['existing_name'] = other_name
                output['results'].append(homoglyph_result)
        else:
            output['results'].append(result)

    return jsonify(output)