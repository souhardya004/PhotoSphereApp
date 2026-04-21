import re

with open(r'c:\PhotoSphere\PhotoApp\templates\PhotoApp\all_photos.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_scroll = False

photo_stats_str = '''                                <div class="mt-3 pt-3 border-t border-gray-100">
                                    <div class="flex justify-between items-center text-sm mb-2">
                                        <span class="flex items-center gap-1 font-semibold text-gray-700">
                                            ❤️ <span id="card-like-count-{{ photo.id }}">{{ photo.like_set.count }}</span>
                                        </span>
                                    </div>
                                    {% with latest_comment=photo.comment_set.last %}
                                        {% if latest_comment %}
                                            <p class="text-xs text-gray-600 truncate"><span class="font-bold text-gray-800">{{ latest_comment.user.username }}:</span> {{ latest_comment.comment }}</p>
                                        {% else %}
                                            <p class="text-xs text-gray-400 italic">No comments yet</p>
                                        {% endif %}
                                    {% endwith %}
                                </div>'''

category_stats_str = '''                                <div class="mt-3 pt-3 border-t border-gray-100">
                                    <div class="flex justify-between items-center text-sm mb-2">
                                        <span class="flex items-center gap-1 font-semibold text-gray-700">
                                            ❤️ <span id="card-like-count-{{ category.title.id }}">{{ category.title.like_set.count }}</span>
                                        </span>
                                    </div>
                                    {% with latest_comment=category.title.comment_set.last %}
                                        {% if latest_comment %}
                                            <p class="text-xs text-gray-600 truncate"><span class="font-bold text-gray-800">{{ latest_comment.user.username }}:</span> {{ latest_comment.comment }}</p>
                                        {% else %}
                                            <p class="text-xs text-gray-400 italic">No comments yet</p>
                                        {% endif %}
                                    {% endwith %}
                                </div>'''

for i, line in enumerate(lines):
    if 'class="horizontal-scroll' in line:
        new_lines.append('            <div class="relative group">\n')
        new_lines.append('                <button onclick="scrollRowLeft(this)" class="absolute left-0 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/80 text-white w-10 h-10 rounded-full z-10 hidden group-hover:flex items-center justify-center -ml-5 shadow-lg transition-all">❮</button>\n')
        new_lines.append('                <button onclick="scrollRowRight(this)" class="absolute right-0 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/80 text-white w-10 h-10 rounded-full z-10 hidden group-hover:flex items-center justify-center -mr-5 shadow-lg transition-all">❯</button>\n')
        new_lines.append(line)
        in_scroll = True
    elif in_scroll and '{% endfor %}' in line:
        # Check if the next line is </div> to close it properly
        next_line = lines[i+1] if i+1 < len(lines) else ''
        if '</div>' in next_line:
            new_lines.append(line)
            # We will handle the extra closing div when we process the next line
        else:
            new_lines.append(line)
    elif in_scroll and '</div>' in line and '{% endfor %}' in lines[i-1]:
        new_lines.append(line)
        new_lines.append('            </div>\n') # Close the relative group wrapper
        in_scroll = False
    elif '<p class="text-gray-500 text-sm">{{ photo.date }}</p>' in line:
        new_lines.append(line)
        new_lines.append(photo_stats_str + '\n')
    elif '<p class="text-gray-500 text-sm">{{ category.title.date }}</p>' in line or '<p class="text-gray-500 text-sm">\n' in line and '{{ category.title.date }}' in lines[i+1]:
        # Handle multi-line date paragraph in category
        new_lines.append(line)
    elif '{{ category.title.date }}' in line and '</p>' in lines[i+1]:
        new_lines.append(line)
    elif '</p>' in line and '{{ category.title.date }}' in lines[i-1]:
        new_lines.append(line)
        new_lines.append(category_stats_str + '\n')
    else:
        new_lines.append(line)

with open(r'c:\PhotoSphere\PhotoApp\templates\PhotoApp\all_photos.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
