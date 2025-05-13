CHAR_FADEIN_ANIMATION_CSS = """   
<style>                    
    /* メッセージ内テキストのfade inアニメーション（containerアニメーション後に開始） */
    /* .st-emotion-cache-4oy321はAI messageのclass名 */
    .st-emotion-cache-4oy321 p,
    .st-emotion-cache-4oy321 span,
    .st-emotion-cache-4oy321 div {
        opacity: 0;
        animation: textFadeIn 1.0s ease forwards;
        animation-delay: 0.0s;
    }
    
    /* テキスト部分のfade in用アニメーション */
    @keyframes textFadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    
</style>
"""