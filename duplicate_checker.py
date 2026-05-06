from difflib import SequenceMatcher

def definitions_are_similar(def1, def2, threshold=0.8):
    similarity = SequenceMatcher(None, def1.lower(), def2.lower()).ratio()
    
    return similarity >= threshold