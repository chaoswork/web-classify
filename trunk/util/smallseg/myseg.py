#encoding=utf-8
from smallseg import SEG

def seg( text ):
    seg = SEG()
    wlist = seg.cut(text)
    word_nums = {}
    
    for w in wlist:
        if len(w)<2:continue
        if word_nums.has_key( w ):
            word_nums[w] += 1
        else:
            word_nums[w] = 1
            
    return word_nums.items()

if __name__ == '__main__':
    text = '手机手机'
    print seg( text )
